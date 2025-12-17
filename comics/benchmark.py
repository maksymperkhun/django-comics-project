import time
import concurrent.futures
from django.db import connections
from .models import Comic


class DatabaseBenchmark:

    @staticmethod
    def _single_db_request(index):
        for conn in connections.all():
            conn.close_if_unusable_or_obsolete()
        _ = Comic.objects.count()
        return index

    @staticmethod
    def run_benchmark(total_requests=200, max_workers_list=[1, 2, 4, 8, 16]):
        results = {
            'workers': [],
            'time': []
        }

        print(f"Starting benchmark with {total_requests} requests...")

        for workers in max_workers_list:
            start_time = time.time()

            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                futures = [executor.submit(DatabaseBenchmark._single_db_request, i) for i in range(total_requests)]

                concurrent.futures.wait(futures)

            end_time = time.time()
            execution_time = end_time - start_time

            results['workers'].append(workers)
            results['time'].append(round(execution_time, 4))

        return results