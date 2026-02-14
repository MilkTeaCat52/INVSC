object q6{
    def tooBig(x:BigInt) : Boolean = {
        (x>1000)
    }
    def determine() : BigInt = {
        // Pre-condition: None
        // Post-condition: returns the number we're guessing
      var l:BigInt = 1;var r:BigInt = 2
      // Invariant: tooBig(l) = false
      // Invariant: r = l * 2, l >= 1
      // Variant: [The actual number we're guessing] * 2 - r
      while(!tooBig(r)){
        r *= 2
        l *= 2
      }
      //tooBig(r)&&Inv => tooBig(r)=true and tooBig(l)=false
      // Invariant: tooBig(r)=true and tooBig(l)=false
      // Variant: r - l
      while(l+1<r){
        val m = (l+r)/2
        if (tooBig(m)) r = m
        else l = m
      }
      //l+1=r and I => tooBig(l+1) = true and tooBig(l) = false
      l
    }
}