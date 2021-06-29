function ReplaceWith(Ele){'use-strict';var parent=this.parentNode,i=arguments.length,firstIsNode=+(parent&&typeof Ele==='object');if(!parent)return;while(i-->firstIsNode){if(parent&&typeof arguments[i]!=='object'){arguments[i]=document.createTextNode(arguments[i]);}if(!parent&&arguments[i].parentNode){arguments[i].parentNode.removeChild(arguments[i]);continue;}
parent.insertBefore(this.previousSibling,arguments[i]);}
if(firstIsNode)parent.replaceChild(Ele,this);}
if(!Element.prototype.replaceWith)
Element.prototype.replaceWith=ReplaceWith;if(!CharacterData.prototype.replaceWith)
CharacterData.prototype.replaceWith=ReplaceWith;if(!DocumentType.prototype.replaceWith)
DocumentType.prototype.replaceWith=ReplaceWith;var tippers=document.querySelectorAll('[to][network][amount]')
if(tippers.length>0){for(i=0;i<tippers.length;i++){var tipper=tippers[i]
var iframe=document.createElement('iframe')
iframe.src='https://www.xrptipbot.com/donate/button?'+
'to='+encodeURIComponent(tipper.getAttribute('to'))+'&'+
'network='+encodeURIComponent(tipper.getAttribute('network'))+'&'+
'amount='+encodeURIComponent(tipper.getAttribute('amount'))+'&'+
'label='+encodeURIComponent(tipper.getAttribute('label'))+'&'+
'labelpt='+encodeURIComponent(tipper.getAttribute('labelpt'))+'&'+
'unique='+encodeURIComponent(tipper.getAttribute('unique'))+'&'+
'redirect='+encodeURIComponent(tipper.getAttribute('redirect'))+'&'+
'stylesheet='+encodeURIComponent(tipper.getAttribute('stylesheet'))
iframe.width='270'
iframe.height='60'
iframe.style.width='270px'
iframe.style.height='60px'
iframe.setAttribute('class','xrptipbot-tipper')
iframe.marginHeight='0'
iframe.align='top'
iframe.scrolling='no'
iframe.frameBorder='0'
iframe.border='0'
iframe.style.border='none'
iframe.hspace='0'
iframe.vspace='0'
iframe.allowTransparency='true'
if(tipper.getAttribute('size')){iframe.width=tipper.getAttribute('size')
iframe.style.width=tipper.getAttribute('size')+'px'}
tipper.replaceWith(iframe)
console.log(tipper.getAttribute('to'),tipper.getAttribute('network'),tipper.getAttribute('amount'))}}