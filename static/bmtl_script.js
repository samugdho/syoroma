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
(function(){
	var TITLE = 0, CH = 1;
	var histDiv = document.querySelector(".history");
	if(histDiv!=null){
		var hist = localStorage.getItem("my_history");
		if(hist == null){
			histDiv.innerHTML = "<p class='gray'>No history</p>"
		}else{
			histDiv.innerHTML = "";
			hist = hist.split("::AND::");
			hist.forEach(function(item){
				var parts = item.split("::PART::");
				histDiv.innerHTML += "<p>"+parts[TITLE]+"|"+parts[CH]+"</p>";
			})
		}
	}
	
	
})();

