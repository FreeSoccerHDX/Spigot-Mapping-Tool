window.onload=function(){

console.log("try something")
	
searchbar = document.getElementById("searchbar");
searchoutput = document.getElementById("searchoutput");

searchbar.addEventListener("onkeyup", onkeyupfunction)
searchbar.onkeyup = onkeyupfunction


function onkeyupfunction(event){
	//console.log("event.key -> " + event.key)
	if(event.key === 'Enter') {
		//console.log("Enter the search!?=!")
	
		var nametofind = searchbar.value.replaceAll("/",";=");
		
		elements = []
		
		document.querySelectorAll('*').forEach(el => {
			
			if(el.id.includes(nametofind)){
				elements.push(el)
			}
		});
		
		searchoutput.innerHTML = "";
		
		var arrayLength = elements.length;
		for (var i = 0; i < arrayLength; i++) {
			var el = elements[i]
		
		
			
			searchoutput.innerHTML += "<p class='sod'><a class='sc' href='#"+el.id+"'>"+el.id.replaceAll(";=","/")+"</a></p>"
			
		};
		
		if(arrayLength == 1){
			elements[0].scrollIntoView();
		}else{
			window.scrollTo(0,0);
		}
		
		//console.log(elements);
		
	}
}
	
	
	
	
}