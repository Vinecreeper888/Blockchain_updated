pragma solidity >=0.5.16;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/Adoption.sol";

contract TestAdoption {
    //The address of the adoption contract
    //to be tested
    Adoption adoption = Adoption(DeployedAddresses.Adoption());

    //id of the pet that will be used for testing
    uint256 expectedPetId = 8;

    //THe expected owner of the adopted pet is this contract
    address expectedAdopter = address(this);

    //Testing adopt function
    function testUserCanAdopt() public {
        uint256 returnedId = adoption.adopt(expectedPetId);
        Assert.equal(
            returnedId,
            expectedPetId,
            "Adoption of the expected pet should match what is returned"
        );

    }

    //testing retrieval of a single pet owner
    function testGetAdopterAddressByPetId() public {
        address adopter = adoption.adopters(expectedPetId);

        Assert.equal(
            adopter,
            expectedAdopter,
            "Owner of the expected pet should be this contract"
        );
    }

    //Testign retrieval of all pet owners
    function testGetAdopterAddressByPetIdinArray() public {
        //store the adopters in memory rather than contract storage
        address[16] memory adopters = adoption.getAdopters();

        Assert.equal(
            adopters[expectedPetId],
            expectedAdopter,
            "Owner of the expected pet should be this contract"
        );
    }
}
