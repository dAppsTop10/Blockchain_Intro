// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
import "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";


contract GetApi is ChainlinkClient {
    using Chainlink for Chainlink.Request;

    uint256 public market_cap;

    bytes32 private jobId;
    uint256 private fee;
    int256 public test_num;


    event RequestFirstId(bytes32 indexed requestId, uint256 market_cap);


    constructor() {
        setChainlinkToken(0x326C977E6efc84E512bB9C30f76E30c160eD06FB); //chainLink address on the testent you are using
        setChainlinkOracle(0xA2e52216e6F2304300D9A3Be439c58299Fb8E330);// your provider address
        jobId ="06b932d62b4b4ad09cef6e05aac6d04e"; //your jobId
        fee = (1 * LINK_DIVISIBILITY) / 10; // 0,1 * 10**18 (Varies by network and job)

    }

    /**
     * Create a Chainlink request to retrieve API response, find the target
     * data which is located in a list
     */

    function requestFirstId() public returns (bytes32 requestId) {
        Chainlink.Request memory req = buildChainlinkRequest(
            jobId,
            address(this),
            this.fulfill.selector
        );

        req.add(
            "get",
              "http://x.x.x.x:5000/api/gw" //your api address
        );

        req.add("path", "result"); // Chainlink nodes 1.0.0 and later support this format
        // Sends the request
        int256 timesAmount = 10 ** 0;
        req.addInt("times", timesAmount);

        return sendChainlinkRequest(req, fee);
    }

    /**
     * Receive the response in the form of string
     */
    function fulfill (
        bytes32 _requestId,
        uint256  _market_cap
    )   public  recordChainlinkFulfillment(_requestId) {
        emit RequestFirstId(_requestId, _market_cap);
        market_cap = _market_cap;


    }

    /**
     * Allow withdraw of Link tokens from the contract
     */


    function withdrawLink() public  {
        LinkTokenInterface link = LinkTokenInterface(chainlinkTokenAddress());
        require(
            link.transfer(msg.sender, link.balanceOf(address(this))),
            "Unable to transfer"
        );
    }
}
