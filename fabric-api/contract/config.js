const Web3 = require("web3");
const fs = require("fs");
const path = require("path");


const contractJson = require("./TrainerLog.json"); 
const contractABI = contractJson.abi;
const contractAddress = "0xCONTRACT_ADDRESS_REPLACEME"; 

const web3 = new Web3("http://ganache:8545"); 

const contract = new web3.eth.Contract(contractABI, contractAddress);

module.exports = { web3, contract };
