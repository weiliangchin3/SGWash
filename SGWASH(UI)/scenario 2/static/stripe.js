const button = document.querySelector("#checkout");
var serviceType = "normal";

document.querySelectorAll('input[name = "serviceType"]').forEach((elem) =>{
    elem.addEventListener("change", function(event){
        var item = event.target.value;
        serviceType = item;
    })
});

button.addEventListener('click', ()=>{
    
    var pCode = $("#postalCode").val();
    var address = $("#address").val();
    var pNum = $("#pNum").val();
    var bookType = $("#bookType").val();
    var description = $("#description").val();
    var cost = 20.50;
    console.log(description);
    console.log(bookType);
    console.log(serviceType);

    var url = "https://location-verification-gateway-48gyfk5q.ts.gateway.dev/validateaddress?key=AIzaSyCfkdAXwQgJcPqgikE6e4sujSb3XbIVFqw&pCode=760458" ;
    console.log(url)
    fetch(url,{
        method: 'GET',
        //headers: {"Access-Control-Allow-Origin": "*" },
        
    }).then( (response) =>{
        if (response.status == "200"){
            fetch(`/payment`,{ method:'POST',
            headers: {"Content-Type": "application/json" },body: JSON.stringify({
            postal : pCode, vAddress:address,carplate:pNum,bookingType:bookType,description:description,serviceType:serviceType
            }), })
            .then((result) =>{
            return result.json();})
            .then((data) =>{
            var stripe = Stripe(data.checkout_public_key);
            stripe.redirectToCheckout({
            sessionId: data.checkout_session_id
            });
            });
        }
        
    }
    
    )

});
