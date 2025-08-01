#!/usr/bin/env python3
"""
Batch Processor Script

This script handles large-scale batch processing of Google Search Trends data.
It can process multiple keywords, locations, and timeframes efficiently.

Features:
- Batch keyword processing
- Parallel processing support
- Progress tracking and resumption
- Data validation and error handling
- Export to multiple formats
- Resource management
"""

import os
import json
import time
import logging
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from pathlib import Path

# Add parent directory to path to import from src
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api_clients.pytrends_client import PyTrendsClient
from src.api_clients.valueserp_client import ValueSerpClient
from src.trends_analyzer import TrendsAnalyzer
from src.data_processors.trends_processor import TrendsDataProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/batch_processor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class BatchProcessor:
    """
    Batch processing class for large-scale trend analysis.
    """
    
    def __init__(self, config_file: str = "config/batch_config.json"):
        """
        Initialize the batch processor.
        
        Args:
            config_file (str): Path to configuration file
        """
        self.config = self.load_config(config_file)
        self.analyzer = TrendsAnalyzer()
        self.pytrends_client = PyTrendsClient()
        self.data_processor = TrendsDataProcessor()
        
        # Initialize Value SERP client if API key is available
        self.valueserp_client = None
        if os.getenv('VALUE_SERP_API_KEY'):
            self.valueserp_client = ValueSerpClient(api_key=os.getenv('VALUE_SERP_API_KEY'))
        
        # Processing state
        self.processed_items = set()
        self.failed_items = []
        self.results = []
        
        # Create output directories
        self.create_output_directories()
        
        logger.info("Batch Processor initialized")
    
    def load_config(self, config_file: str) -> Dict[str, Any]:
        """
        Load configuration from JSON file.
        
        Args:
            config_file (str): Path to configuration file
            
        Returns:
            Dict containing configuration
        """
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {config_file}")
            return config
        except FileNotFoundError:
            logger.warning(f"Config file {config_file} not found, using defaults")
            return self.get_default_config()
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing config file: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration.
        
        Returns:
            Default configuration dictionary
        """
        return {
            "keywords": [
                "artificial intelligence", "machine learning", "python",
                "data science", "deep learning", "neural networks",
                "blockchain", "cryptocurrency", "bitcoin", "ethereum",
                "cloud computing", "aws", "azure", "google cloud",
                "cybersecurity", "privacy", "gdpr", "data protection"
            ],
            "locations": ["US", "GB", "CA", "AU", "DE", "FR", "JP", "IN"],
            "timeframes": ["today 1-m", "today 3-m", "today 12-m"],
            "processing": {
                "max_workers": 4,
                "batch_size": 5,
                "delay_between_batches": 2,
                "retry_attempts": 3,
                "retry_delay": 5
            },
            "output": {
                "format": ["json", "csv", "excel"],
                "directory": "data/batch_results/",
                "include_metadata": True,
                "compress_results": False
            },
            "validation": {
                "min_data_points": 10,
                "max_missing_values": 0.2,
                "validate_trends": True
            }
        }
    
    def create_output_directories(self):
        """Create necessary output directories."""
        output_dir = self.config['output']['directory']
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        os.makedirs('data/temp', exist_ok=True)
    
    def generate_batch_tasks(self) -> List[Dict[str, Any]]:
        """
        Generate batch processing tasks from configuration.
        
        Returns:
            List of task dictionaries
        """
        tasks = []
        
        for keyword in self.config['keywords']:
            for location in self.config['locations']:
                for timeframe in self.config['timeframes']:
                    task = {
                        'keyword': keyword,
                        'location': location,
                        'timeframe': timeframe,
                        'task_id': f"{keyword}_{location}_{timeframe.replace(' ', '_')}"
                    }
                    tasks.append(task)
        
        logger.info(f"Generated {len(tasks)} batch tasks")
        return tasks
    
    def process_single_task(self, task: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single batch task.
        
        Args:
            task (Dict): Task dictionary
            
        Returns:
            Processing result or None if failed
        """
        task_id = task['task_id']
        
        try:
            logger.info(f"Processing task: {task_id}")
            
            # Get trend data
            payload = {
                'kw_list': [task['keyword']],
                'geo': task['location'],
                'timeframe': task['timeframe']
            }
            
            data = self.pytrends_client.get_interest_over_time(payload)
            
            if data is None or data.empty:
                logger.warning(f"No data for task: {task_id}")
                return None
            
            # Process the data
            processed_data = self.data_processor.process_trends_data(data)
            
            # Validate the data
            if not self.validate_data(processed_data, task):
                logger.warning(f"Data validation failed for task: {task_id}")
                return None
            
            # Prepare result
            result = {
                'task_id': task_id,
                'keyword': task['keyword'],
                'location': task['location'],
                'timeframe': task['timeframe'],
                'data': processed_data.to_dict('records'),
                'metadata': {
                    'processed_at': datetime.now().isoformat(),
                    'data_points': len(processed_data),
                    'date_range': {
                        'start': processed_data.index.min().isoformat() if not processed_data.empty else None,
                        'end': processed_data.index.max().isoformat() if not processed_data.empty else None
                    }
                }
            }
            
            logger.info(f"Successfully processed task: {task_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error processing task {task_id}: {e}")
            self.failed_items.append({
                'task_id': task_id,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return None
    
    def validate_data(self, data: pd.DataFrame, task: Dict[str, Any]) -> bool:
        """
        Validate processed data.
        
        Args:
            data (pd.DataFrame): Processed data
            task (Dict): Original task
            
        Returns:
            True if data is valid
        """
        validation_config = self.config['validation']
        
        # Check minimum data points
        if len(data) < validation_config['min_data_points']:
            logger.warning(f"Insufficient data points for {task['task_id']}: {len(data)}")
            return False
        
        # Check for missing values
        missing_ratio = data.isnull().sum().sum() / (len(data) * len(data.columns))
        if missing_ratio > validation_config['max_missing_values']:
            logger.warning(f"Too many missing values for {task['task_id']}: {missing_ratio:.2%}")
            return False
        
        # Validate trends if enabled
        if validation_config['validate_trends']:
            for column in data.columns:
                if column != 'date':
                    values = data[column].dropna()
                    if len(values) > 0:
                        # Check if all values are numeric and reasonable
                        if not pd.api.types.is_numeric_dtype(values):
                            logger.warning(f"Non-numeric values in {task['task_id']}: {column}")
                            return False
                        
                        # Check for reasonable range (0-100 for Google Trends)
                        if values.max() > 100 or values.min() < 0:
                            logger.warning(f"Values out of range for {task['task_id']}: {column}")
                            return False
        
        return True
    
    def process_batch(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process a batch of tasks using parallel processing.
        
        Args:
            tasks (List): List of tasks to process
            
        Returns:
            List of successful results
        """
        max_workers = self.config['processing']['max_workers']
        results = []
        
        logger.info(f"Processing batch of {len(tasks)} tasks with {max_workers} workers")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_task = {executor.submit(self.process_single_task, task): task for task in tasks}
            
            # Process completed tasks
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    if result is not None:
                        results.append(result)
                        self.processed_items.add(task['task_id'])
                except Exception as e:
                    logger.error(f"Task {task['task_id']} generated an exception: {e}")
                    self.failed_items.append({
                        'task_id': task['task_id'],
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    })
        
        logger.info(f"Batch completed: {len(results)} successful, {len(self.failed_items)} failed")
        return results
    
    def save_results(self, results: List[Dict[str, Any]], batch_id: str):
        """
        Save batch results to files.
        
        Args:
            results (List): List of results to save
            batch_id (str): Batch identifier
        """
        output_config = self.config['output']
        output_dir = output_config['directory']
        
        # Prepare data for export
        export_data = {
            'batch_id': batch_id,
            'processed_at': datetime.now().isoformat(),
            'total_results': len(results),
            'results': results
        }
        
        if output_config['include_metadata']:
            export_data['metadata'] = {
                'config': self.config,
                'failed_items': self.failed_items,
                'processing_stats': {
                    'total_processed': len(self.processed_items),
                    'total_failed': len(self.failed_items)
                }
            }
        
        # Save in different formats
        for format_type in output_config['format']:
            try:
                if format_type == 'json':
                    filename = f"{output_dir}batch_{batch_id}.json"
                    with open(filename, 'w') as f:
                        json.dump(export_data, f, indent=2, default=str)
                
                elif format_type == 'csv':
                    # Flatten results for CSV export
                    flat_data = []
                    for result in results:
                        for data_point in result['data']:
                            flat_data.append({
                                'task_id': result['task_id'],
                                'keyword': result['keyword'],
                                'location': result['location'],
                                'timeframe': result['timeframe'],
                                **data_point
                            })
                    
                    if flat_data:
                        df = pd.DataFrame(flat_data)
                        filename = f"{output_dir}batch_{batch_id}.csv"
                        df.to_csv(filename, index=False)
                
                elif format_type == 'excel':
                    filename = f"{output_dir}batch_{batch_id}.xlsx"
                    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                        # Summary sheet
                        summary_data = []
                        for result in results:
                            summary_data.append({
                                'task_id': result['task_id'],
                                'keyword': result['keyword'],
                                'location': result['location'],
                                'timeframe': result['timeframe'],
                                'data_points': result['metadata']['data_points'],
                                'date_range_start': result['metadata']['date_range']['start'],
                                'date_range_end': result['metadata']['date_range']['end']
                            })
                        
                        df_summary = pd.DataFrame(summary_data)
                        df_summary.to_excel(writer, sheet_name='Summary', index=False)
                        
                        # Data sheet (flattened)
                        flat_data = []
                        for result in results:
                            for data_point in result['data']:
                                flat_data.append({
                                    'task_id': result['task_id'],
                                    'keyword': result['keyword'],
                                    'location': result['location'],
                                    'timeframe': result['timeframe'],
                                    **data_point
                                })
                        
                        if flat_data:
                            df_data = pd.DataFrame(flat_data)
                            df_data.to_excel(writer, sheet_name='Data', index=False)
                
                logger.info(f"Results saved in {format_type} format: {filename}")
                
            except Exception as e:
                logger.error(f"Error saving results in {format_type} format: {e}")
    
    def run_batch_processing(self, resume_from: Optional[str] = None):
        """
        Run the complete batch processing workflow.
        
        Args:
            resume_from (str): Resume from a specific batch ID
        """
        logger.info("Starting batch processing")
        
        # Generate tasks
        all_tasks = self.generate_batch_tasks()
        
        # Filter out already processed tasks if resuming
        if resume_from:
            logger.info(f"Resuming from batch: {resume_from}")
            # Load previous state and filter tasks
            # This is a simplified implementation
            pass
        
        # Process in batches
        batch_size = self.config['processing']['batch_size']
        delay = self.config['processing']['delay_between_batches']
        
        total_batches = (len(all_tasks) + batch_size - 1) // batch_size
        batch_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        logger.info(f"Processing {len(all_tasks)} tasks in {total_batches} batches")
        
        for i in range(0, len(all_tasks), batch_size):
            batch_num = (i // batch_size) + 1
            batch_tasks = all_tasks[i:i + batch_size]
            
            logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch_tasks)} tasks)")
            
            # Process batch
            batch_results = self.process_batch(batch_tasks)
            self.results.extend(batch_results)
            
            # Save intermediate results
            if batch_results:
                self.save_results(batch_results, f"{batch_id}_batch_{batch_num}")
            
            # Delay between batches
            if i + batch_size < len(all_tasks):
                logger.info(f"Waiting {delay} seconds before next batch...")
                time.sleep(delay)
        
        # Save final results
        if self.results:
            self.save_results(self.results, f"{batch_id}_complete")
        
        # Generate summary report
        self.generate_summary_report(batch_id)
        
        logger.info("Batch processing completed")
    
    def generate_summary_report(self, batch_id: str):
        """
        Generate a summary report of the batch processing.
        
        Args:
            batch_id (str): Batch identifier
        """
        report = {
            'batch_id': batch_id,
            'processing_summary': {
                'total_tasks': len(self.config['keywords']) * len(self.config['locations']) * len(self.config['timeframes']),
                'successful_tasks': len(self.processed_items),
                'failed_tasks': len(self.failed_items),
                'success_rate': len(self.processed_items) / (len(self.processed_items) + len(self.failed_items)) * 100
            },
            'processing_time': {
                'started_at': datetime.now().isoformat(),
                'completed_at': datetime.now().isoformat()
            },
            'failed_items': self.failed_items,
            'configuration': {
                'keywords_count': len(self.config['keywords']),
                'locations_count': len(self.config['locations']),
                'timeframes_count': len(self.config['timeframes'])
            }
        }
        
        # Save report
        report_file = f"{self.config['output']['directory']}report_{batch_id}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Summary report saved: {report_file}")
        
        # Print summary
        print("\n" + "="*50)
        print("BATCH PROCESSING SUMMARY")
        print("="*50)
        print(f"Total Tasks: {report['processing_summary']['total_tasks']}")
        print(f"Successful: {report['processing_summary']['successful_tasks']}")
        print(f"Failed: {report['processing_summary']['failed_tasks']}")
        print(f"Success Rate: {report['processing_summary']['success_rate']:.1f}%")
        print("="*50)


def main():
    """Main function to run batch processing."""
    parser = argparse.ArgumentParser(description='Batch process Google Search Trends data')
    parser.add_argument('--config', '-c', default='config/batch_config.json',
                       help='Configuration file path')
    parser.add_argument('--resume', '-r', help='Resume from batch ID')
    parser.add_argument('--keywords', '-k', nargs='+', help='Keywords to process')
    parser.add_argument('--locations', '-l', nargs='+', help='Locations to process')
    parser.add_argument('--timeframes', '-t', nargs='+', help='Timeframes to process')
    
    args = parser.parse_args()
    
    print("🚀 Starting Google Search Trends Batch Processor")
    print("=" * 60)
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Initialize and run processor
    processor = BatchProcessor(args.config)
    
    # Override config with command line arguments
    if args.keywords:
        processor.config['keywords'] = args.keywords
    if args.locations:
        processor.config['locations'] = args.locations
    if args.timeframes:
        processor.config['timeframes'] = args.timeframes
    
    processor.run_batch_processing(resume_from=args.resume)


if __name__ == "__main__":
    main() 