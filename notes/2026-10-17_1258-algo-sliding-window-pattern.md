# Sliding Window Pattern for Efficient Subarray Processing

- **Date:** 2026-10-17 12:58 WIB
- **Category:** `Algorithms`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### Sliding Window Pattern for Efficient Subarray Processing

Calculating properties over contiguous subarrays using nested loops takes $O(N^2)$ time. The sliding window technique maintains rolling state in $O(N)$ linear time.

```python
def max_subarray_sum(nums: list[int], k: int) -> int:
    if len(nums) < k:
        return 0
    window_sum = sum(nums[:k])
    max_sum = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum
```

**Key Takeaway:** Use sliding window whenever computing metrics over fixed or variable contiguous sequences.
