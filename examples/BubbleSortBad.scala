// Example: Bubble Sort WITHOUT invariants (should get a bad grade!)
// Try running: invsc examples/BubbleSortBad.scala

object BubbleSortBad {
  def bubbleSort(arr: Array[Int]): Unit = {
    val n = arr.length
    var i = 0
    while (i < n - 1) {
      var j = 0
      while (j < n - i - 1) {
        if (arr(j) > arr(j + 1)) {
          val temp = arr(j)
          arr(j) = arr(j + 1)
          arr(j + 1) = temp
        }
        j += 1
      }
      i += 1
    }
  }

  def main(args: Array[String]): Unit = {
    val arr = Array(64, 34, 25, 12, 22, 11, 90)
    bubbleSort(arr)
    println("Sorted: " + arr.mkString(", "))
  }
}
