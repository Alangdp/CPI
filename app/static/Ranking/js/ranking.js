function detalhes(){
    var ticker = prompt("Digite o ticker: ")
    if(!ticker ){
        alert('Ticker inválido');
    }if(ticker.length > 6){
        alert('Ticker inválido');
    }if(ticker.length < 5){
        alert('Ticker inválido')
    }else{
        alert('Ticker válido')
        location.href = `/detalhes?ticker=${ticker}`;
    }
}

function Deslogar() {
    const botaoSair = document.getElementById('sair');

    botaoSair.addEventListener('click', (e) => {
        e.preventDefault();
        
        cleanCookie('email');
        cleanCookie('senha');

        window.location.replace("/");
    })
}

function cleanCookie(nome) {
    document.cookie = `${nome}=John Smith; expires=Thu, 18 Dec 2013 12:00:00 UTC; path=/`;
}
Deslogar()