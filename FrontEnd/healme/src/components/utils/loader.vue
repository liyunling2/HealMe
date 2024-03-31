<template>
    <div class="loader-container">
        <div class="lds-dual-ring"></div>
    </div>
</template>

<style>
    .loader-container {
        display: flex;
        justify-content: center; /* Center horizontally */
        align-items: center; /* Center vertically */
        height: 100vh; /* Provide a full viewport height to the parent container */
    }

    .lds-dual-ring {
        display: inline-block;
        width: 80px;
        height: 80px;
    }

    .lds-dual-ring:after {
        content: " ";
        display: block;
        width: 64px;
        height: 64px;
        margin: 8px;
        border-radius: 50%;
        border: 6px solid #29B6F6; /* Red color */
        border-color: #29B6F6 transparent #29B6F6 transparent; /* Red and transparent sections */
        animation: lds-dual-ring 1.2s linear infinite;
    }

    @keyframes lds-dual-ring {  
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
</style>
