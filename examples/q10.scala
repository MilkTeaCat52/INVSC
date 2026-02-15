object q10{

    def partition(l: Int, r: Int) : (Int,Int) = {
        val x = a(l) // pivot
        // Invariant a[l..i) < x = a[i...j) < a[k..r) && l <= i < j <= k <= r
        // && a[0..l) = a_0[0..l) && a[r..N) = a_0[r..N)
        // && a[l..r) is a permutation of a_0[l..r)
        // Variant: k-j
        var i = l; var j = l+1; var k = r
        while(j < k){
            if(a(j) < x){
                //a[i..j)=x, a(j)<x, so we swap a(i) and a(j)
                a(i) = a(j); a(j) = x;
                i += 1; j += 1
            }else if(a(j)==x){
                j += 1
            }
            else{
                //a[k..r)>x, a(j)>x, so we extend [k..r) by swapping a(j) and a(k-1). 
                val t = a(j); a(j) = a(k-1); a(k-1) = t; k -= 1
            }
        }
        //j=k, so a[l..i) < x = a[i...j) < a[j..r)
        (i,j)
    }
}
