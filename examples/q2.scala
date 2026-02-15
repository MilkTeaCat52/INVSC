object q2{
    /** Find integer */
    def sqrt(x: Int) : Int = {
        // invariant I: i^2 <= x < j^2 && 0 <= i < j <= 46341
        var i = 0; var j = 46341 //46340 is the largest integer such that its square is within Int range
        while(i+1 < j){
            //j-i>=2, so step != 0
            val step = (j-i+2)/3;//ceil((j-i)/3)
            val m1 = i + step; val m2 = j - step//i<m1<=m2<j<=43641
            if(m1*m1 > x){
                j = m1
            } else {
                if(m2*m2 > x){
                    i = m1
                    j = m2
                }else{
                    i = m2 
                }
            }
            assert(i!=j)
        }
        // I && i + 1 >= j => i^2<=x<(i+1)^2
        i
    }
    
    // Find a s.t. a^2 <= y < (a+1)^2.  Precondition: y >= 0.
    def binSqrt(y:Int) : Int = {
        require(y >= 0)
        // Deal with y=0 or 1
        if (y <= 1) return y
        // Invariant I: a^2 <= y < b^2 and 0 <= a < b
        var a = 0; var b = y
        while(a+1 < b){
            val m = a + (b-a)/2 // a < m < b
            if(m*m <= y) a = m else b = m
        }
        // I and a+1=b, so a^2 <= y < (a+1)^2
        return a
    }
    def check1() : Unit = {
        for(y <- 0 until 46000){
            try{
                assert(sqrt(y) == binSqrt(y) )
            } catch {
                case _ : Throwable => {
                    println(s"$y : binsqrt = ${binSqrt(y)}, sqrt = ${sqrt(y)}")
                }
            }
        }
    }
    def check2() : Unit = {
        for(y <- 0 to 100000000){
            val x = sqrt(y)
            assert(x*x<=y&&y<(x+1)*(x+1))
        }
    }
    def main(args:Array[String]) : Unit = {
        println(sqrt(2147483647))
        check2();
    }
}
