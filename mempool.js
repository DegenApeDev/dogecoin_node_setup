const { exec } = require('child_process');

function runDogecoinCli(command) {
  return new Promise((resolve, reject) => {
    exec(`dogecoin-cli ${command}`, (error, stdout, stderr) => {
      if (error) {
        reject(`Error executing command: ${error}`);
        return;
      }
      resolve(stdout.trim());
    });
  });
}

function runCurl(txid) {
  return new Promise((resolve, reject) => {
    const apiUrl = `http://127.0.0.1:3000/tx/${txid}`;
    exec(`curl ${apiUrl}`, (error, stdout, stderr) => {
      if (error) {
        reject(`Error running curl command: ${error}`);
        return;
      }
      resolve(stdout.trim());
    });
  });
}

async function processTransactions() {
  try {
    // Get raw mempool transactions
    const rawMempoolOutput = await runDogecoinCli('getrawmempool');
    const mempoolTransactions = JSON.parse(rawMempoolOutput);

    console.log("Mempool Transactions:");
    for (const txid of mempoolTransactions) {
      console.log(`Transaction ID: ${txid}`);

      // Run the curl command
      const curlResult = await runCurl(txid);
      console.log(curlResult);
      console.log();
    }
  } catch (error) {
    console.error(error);
  }
}

// Run the main function
processTransactions();
