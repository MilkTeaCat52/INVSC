
def log3(x : Int): Int = {
  var nx:Int = x; var y = 0
  //Invariant: floor(log3(x)) = y + floor(log3(nx)) and 1<=nx<=x
  while(nx>1){
    //floor(log3(nx)) = 1 + floor(log3(nx/3)) = 1 + floor(log3(floor(nx/3)))
    nx = (nx/3)
    y += 1
  }
  //Variant: nx
  //not(nx>1) and (1<=nx<=x) gives nx=1
  //So floor(log3(x)) = y + floor(log3(0)) = y
  y
}