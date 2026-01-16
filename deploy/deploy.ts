import { readFileSync } from 'fs';

export default async function main(client) {
    console.log("Deploying Dispute Resolution Contract...");

    const contractCode = readFileSync(
        "contracts/dispute_resolution.py",
        "utf-8"
    );

    const deployTransaction = await client.deployContract({
        code: contractCode,
        args: []
    });

    console.log("Waiting for deployment...");
    const receipt = await client.waitForTransactionReceipt({
        hash: deployTransaction,
        status: "FINALIZED"
    });

    console.log(`Contract deployed at: ${receipt.contractAddress}`);
    return receipt.contractAddress;
}
