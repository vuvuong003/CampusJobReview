let base_url = "https://fd30-2405-201-17-f0cf-ccb4-96dd-8fce-bbbf.ngrok-free.app"

export let login_url = base_url + "/auth/token/";
export let register_url = base_url + "/auth/register/";
export let review_url = base_url + "/service/reviews/";
export let filter_url = base_url + "/service/filter";

export let unprotected_api_call = async (url, data={}, type="POST") => {
    try{
        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");

        let raw
        let requestOptions

        if(type === "GET"){
            requestOptions = {
                method: 'GET',
                redirect: 'follow',
                headers: myHeaders
            };
        }else{
            raw = JSON.stringify(data);
            requestOptions = {
                method: type,
                headers: myHeaders,
                body: raw,
                redirect: "follow"
            };    
        }
        
        let response = await fetch(url, requestOptions);
        return response;
    }catch(e){
        console.log(e);
        alert("Server Error")
    }
}

export let protected_api_call = async (url, data={}, type="POST") => {
    try{
        let token = localStorage.getItem("user_data");
        token = JSON.parse(token)["data"]["tokens"]["access"];
        var myHeaders = new Headers();
        myHeaders.append("Authorization", "Bearer " + token);
        myHeaders.append("Content-Type", "application/json");

        let raw
        let requestOptions


        if(type === "GET"){
            requestOptions = {
                method: 'GET',
                redirect: 'follow',
                headers: myHeaders
            };
        }else{
            raw = JSON.stringify(data);
            requestOptions = {
                method: type,
                headers: myHeaders,
                body: raw,
                redirect: "follow"
            };    
        }
        
        let response = await fetch(url, requestOptions);
        console.log(response);
        return response;
    }catch(e){
        console.log(e);
        alert("Server Error")
    }
}