//click to reveal
document.addEventListener("click", function(e){
	var f = e.target;
	var p = e.target.parentNode;
	if(f.classList.contains('f')){
		p.classList.add('see')
	}else if(f.classList.contains('r')){
		p.classList.remove('see')
	}
})

document.addEventListener('DOMContentLoaded', function(){ 
    var t = localStorage.getItem('theme');
	var a = 'white'
	if(t==a){
		document.body.classList.add(a);
	}

}, false);

var reqPart = function(part, total){
	var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.body.innerHTML = document.body.innerHTML +this.responseText;
    }
  };
  xhttp.open("GET", "getPart/part="+part+"&total="+total, true);
  xhttp.send();
};

