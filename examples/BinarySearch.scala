// Example: Binary Search with proper invariants (should get α)
// Try running: invsc examples/BinarySearch.scala

object BinarySearch {
  // Pre-condition: arr is sorted in ascending order
  // Post-condition: returns index of target if found, -1 otherwise
  def binarySearch(arr: Array[Int], target: Int): Int = {
    var lo = 0
    var hi = arr.length - 1

    // Invariant: if target is in arr, then arr(lo) <= target <= arr(hi)
    // Variant: hi - lo
    while (lo <= hi) {
      val mid = lo + (hi - lo) / 2
      if (arr(mid) == target) {
        return mid
      } else if (arr(mid) < target) {
        lo = mid + 1
      } else {
        hi = mid - 1
      }
    }

    -1
  }

  def main(args: Array[String]): Unit = {
    val arr = Array(1, 3, 5, 7, 9, 11, 13)
    val target = 7

    val result = binarySearch(arr, target)
    if (result != -1) {
      println(s"Found $target at index $result")
    } else {
      println(s"$target not found")
    }
  }
}
