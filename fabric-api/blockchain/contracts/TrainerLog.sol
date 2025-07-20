// contracts/TrainerLog.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TrainerLog {
    event RoundLogged(uint256 round, string accuracy, string loss, uint256 timestamp);

    struct TrainingRound {
        uint256 round;
        string accuracy;
        string loss;
        uint256 timestamp;
    }

    TrainingRound[] public rounds;

    function logTrainingRound(
        uint256 _round,
        string memory _accuracy,
        string memory _loss,
        uint256 _timestamp
    ) public {
        rounds.push(TrainingRound(_round, _accuracy, _loss, _timestamp));
        emit RoundLogged(_round, _accuracy, _loss, _timestamp);
    }

    function getRoundCount() public view returns (uint256) {
        return rounds.length;
    }

    function getRound(uint256 index) public view returns (uint256, string memory, string memory, uint256) {
        require(index < rounds.length, "Index out of range");
        TrainingRound memory r = rounds[index];
        return (r.round, r.accuracy, r.loss, r.timestamp);
    }
}
