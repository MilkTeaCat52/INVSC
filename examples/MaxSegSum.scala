object MaxSegSum{
  // Pre: 0 <= p <= q <= a.size
  // Post: returns sum a[p..q).  
  def segsum(a: Array[Int], p: Int, q: Int) : Int = {
    var sum = 0; var i = p
    while (i < q){ sum += a(i); i += 1 }
    sum
  }


  // Calculate max{segsum(a,p,q) | 0 <= p <= q <= a.size}
  // This version is O(N^3)
  def maxsegsum1(a:Array[Int]) : Int = {
    val N = a.size
    var mss = 0; var n = 0
    // Invariant I: mss = max{segsum(a,p,q) | 0 <= p <= q <= n} 
    //              && 0 <= n <= N
    while(n<N){
      n = n+1
      // Consider segsum(a,p,n) for 0 <= p <= n
      var m = 0
      // Invariant:
      // J = mss = max( {segsum(a,p,q) | 0 <= p <= q < n} U
      //                {segsum(a,p,n) | 0 <= p < m} )
      // && 0 <= m <= n+1 && n <= N
      while(m<=n){
        mss = mss max segsum(a,m,n)
        m = m+1
      }
      // mss = max( {segsum(a,p,q) | 0 <= p <= q < n} U
      //            {segsum(a,p,n) | 0 <= p <= n} )
      //     = max{segsum(a,p,q) | 0 <= p <= q <= n}
    }
    mss
  }

  // This version is O(N^2)
  def maxsegsum2(a:Array[Int]) : Int = {
    val N = a.size;
    var mss = 0; var n = 0;
    // Invariant I: mss = max{segsum(a,p,q) | 0 <= p <= q <= n} && 0 <= n <= N
    while(n<N){
      n = n+1
      // Consider all segsum(a,p,n) for 0 <= p <= n
      var m = n; var ss = 0 // mss = mss max ss -- no need
      // Invariant: J where
      // J = mss = max( {segsum(a,p,q) | 0 <= p <= q < n} U
      //                {segsum(a,p,n) | m <= p <= n} )
      // && 0 <= m <= n <= N && ss = seqsum(a,m,n)
      while(m>0){
        m = m-1
        ss = ss + a(m)
        mss = mss max ss
      }
      // mss = max( {segsum(a,p,q) | 0 <= p <= q < n} U
      //            {segsum(a,p,n) | 0 <= p <= n} )
      //     = max{segsum(a,p,q) | 0 <= p <= q <= n}
    }
    mss
  }

  // This version is O(N)
  def maxsegsum3(a:Array[Int]) : Int = {
    val N = a.size;
    var n = 0; var mss = 0; var mrss = 0
    // Invariant: mss = max{segsum(a,p,q) | 0 <= p <= q <= n} && 0 <= n <= N
    // && mrss = max{segsum(a,p,n) | 0 <= p <= n}
    while(n<N){
      n = n+1
      mrss = (mrss + a(n-1)) max 0
      mss = mss max mrss
    }
    mss
  }

  /*
   * Simple driver: Take all command line arguments as the array to examine.  Hard coded method
   *
  def main(args:Array[String]) : Unit = println(maxsegsum3(args.map(_.toInt)))
   */


  // Print array
  def printArray(a : Array[Int]) : Unit = {
    for(i <- 0 until a.size) print(a(i).toString+"\t")
    println()
  }
  // This driver selects a method and a size of array
  def main(args: Array[String]) : Unit = {
    assert (args.size > 0, "Usage: scala MaxSegSum #ItemsInArray #Method")
    var N = args(0).toInt // # elements in array
    val a = new Array[Int](N)
    val range = 100
    val random = new scala.util.Random
    for(i <- 0 until N) a(i) = random.nextInt(2*range)-range

    if(N <= 100) printArray(a)

    val t0 = java.lang.System.currentTimeMillis()
    var alg = "All"
    if (args.size>1) alg=args(1)
    alg match{
      case "1" => println(maxsegsum1(a))
      case "2" => println(maxsegsum2(a))
      case "3" => println(maxsegsum3(a))
      case  _  => {
         val ts3 = java.lang.System.currentTimeMillis(); println(maxsegsum3(a).toString + "   Alg 3; O(n);   Time: "+ (java.lang.System.currentTimeMillis()-ts3))
         val ts2 = java.lang.System.currentTimeMillis(); println(maxsegsum2(a).toString + "   Alg 2; O(n^2); Time: "+ (java.lang.System.currentTimeMillis()-ts2))
         val ts1 = java.lang.System.currentTimeMillis(); println(maxsegsum1(a).toString + "   Alg 1; O(n^3); Time: "+ (java.lang.System.currentTimeMillis()-ts1))
      }
    }
    val t1 = java.lang.System.currentTimeMillis()
    println("Time: "+ (t1-t0))
  }

}