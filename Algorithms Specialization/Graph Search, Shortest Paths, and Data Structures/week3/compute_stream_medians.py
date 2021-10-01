"""
we want to have 2 heaps
# one will always return the max element
# one will always return the min element
# for example, [3, 1, 10, 100, 11, 15]

# max_heap = [1, 3, 10]
# min_heap = [11, 100]


# first number is 3
# if heap has the same number of elements, push to max
# else push to min
# since heaps always store the min, to get the max, we change to a negative
# -3 -1 -10 > min will -10 (and its absolute is therefore the max)
"""

import heapq
import time


class MedianStream:
    def __init__(self):
        self.max_heap = []
        heapq.heapify(self.max_heap)
        self.min_heap = []
        heapq.heapify(self.min_heap)

    def add_element(self, value):
        len_max_heap = len(self.max_heap)
        len_min_heap = len(self.min_heap)

        # scenarios
        if len_max_heap == 0 and len_min_heap == 0:
            heapq.heappush(self.max_heap, -value)
            return
        elif len_max_heap > 0 and len_min_heap == 0:
            max_lower_val = -heapq.heappop(self.max_heap)
            if value < max_lower_val:
                heapq.heappush(self.max_heap, -value)
                heapq.heappush(self.min_heap, max_lower_val)
            return

        max_lower_val = -heapq.heappop(self.max_heap)
        min_higher_val = heapq.heappop(self.min_heap)
        # always ensure max_heap has >= min_heap length
        if len_max_heap > len_min_heap:
            # there is one more item in max_heap than min_heap
            # see if we need to move elements around
            if value < max_lower_val:
                # put value into max_heap
                heapq.heappush(self.max_heap, -value)
                # push the other 2 values into min_heap
                heapq.heappush(self.min_heap, max_lower_val)
                heapq.heappush(self.min_heap, min_higher_val)
            else:
                # put value into max_heap
                heapq.heappush(self.max_heap, -max_lower_val)
                # push the other 2 values into min_heap
                heapq.heappush(self.min_heap, value)
                heapq.heappush(self.min_heap, min_higher_val)
        else:
            # len_max_heap == len_min_heap
            if value > min_higher_val:
                heapq.heappush(self.max_heap, -max_lower_val)
                heapq.heappush(self.max_heap, -min_higher_val)
                heapq.heappush(self.min_heap, value)
            else:
                heapq.heappush(self.max_heap, -max_lower_val)
                heapq.heappush(self.max_heap, -value)
                heapq.heappush(self.min_heap, min_higher_val)

    def get_median(self):
        """
        Slightly different definition of median:
        If k is odd, then mk is ((k+1)/2)th smallest number among x1,...,xk
        If k is even, then mk is the (k/2)th smallest number among x1,...,xk
        """
        # max_heap should always have >= number of elements as min_heap
        return -self.max_heap[0]


if __name__ == '__main__':
    median_stream = MedianStream()
    medians_sum = 0

    with open('week3/median.txt', 'r') as f:
        current_value = f.readline()
        while current_value:
            median_stream.add_element(int(current_value))
            current_median = median_stream.get_median()
            medians_sum += current_median
            # print(
            #     'max_heap', median_stream.max_heap,
            #     'min_heap', median_stream.min_heap,
            #     'abs_max_heap_min', median_stream.max_heap and -median_stream.max_heap[0],
            #     'min_heap_min', median_stream.min_heap and median_stream.min_heap[0],
            #     'current_median', current_median,
            #     'medians_sum', medians_sum
            # )
            # time.sleep(1)
            current_value = f.readline()
    print(medians_sum % 10000)


