function mytoggle(obj,toggleID){
        parentEle = document.getElementById(toggleID.id).parentNode;
        pE        = document.getElementById(obj.id).parentNode;
        for(var i=0; i<pE.childNodes.length; i++){
                var temp = pE.childNodes[i];
                if(temp.tagName == 'A')
                {
                console.log(temp);
                        temp.setAttribute('class','');
                }
        }
        obj.setAttribute('class','tab-current');
        for(var i=0; i<parentEle.childNodes.length; i++){
                var temp = parentEle.childNodes[i];
                if(temp.tagName == 'DIV')
                        temp.style.display = "none";
        }
        document.getElementById(toggleID.id).style.display = "block";
};

