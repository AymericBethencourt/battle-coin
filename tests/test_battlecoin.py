import pytest

from chia.types.spend_bundle import SpendBundle
from chia.types.condition_opcodes import ConditionOpcode

from battlecoin.battlecoin_drivers import (
    create_battlecoin_puzzle,
    solution_for_battlecoin,
    battlecoin_announcement_assertion,
)
from cdv.test import setup as setup_test

class TestStandardTransaction:
    @pytest.fixture(scope="function")
    async def setup(self):
        network, alice, bob = await setup_test()
        yield network, alice, bob

    async def make_and_spend_battlecoin(self, network, alice, bob, CONTRIBUTION_AMOUNT):
        # Get our alice wallet some money
        await network.farm_block(farmer=alice)

        # This will use one mojo to create our battlecoin on the blockchain.
        battlecoin_coin = await alice.launch_smart_coin(create_battlecoin_puzzle(1000000000000, bob.puzzle_hash))
        # This retrieves us a coin that is at least 500 mojos.
        contribution_coin = await alice.choose_coin(CONTRIBUTION_AMOUNT)

        #This is the spend of the battlecoin bank coin.  We use the driver code to create the solution.
        battlecoin_spend = await alice.spend_coin(
            battlecoin_coin,
            pushtx=False,
            args=solution_for_battlecoin(battlecoin_coin.as_coin(), CONTRIBUTION_AMOUNT),
        )
        # This is the spend of a standard coin.  We simply spend to ourselves but minus the CONTRIBUTION_AMOUNT.
        contribution_spend = await alice.spend_coin(
            contribution_coin,
            pushtx=False,
            amt=(contribution_coin.amount - CONTRIBUTION_AMOUNT),
            custom_conditions=[
                [ConditionOpcode.CREATE_COIN, contribution_coin.puzzle_hash, (contribution_coin.amount - CONTRIBUTION_AMOUNT)],
                battlecoin_announcement_assertion(battlecoin_coin.as_coin(), CONTRIBUTION_AMOUNT)
            ]
        )

        # Aggregate them to make sure they are spent together
        combined_spend = SpendBundle.aggregate([contribution_spend, battlecoin_spend])

        result = await network.push_tx(combined_spend)
        return result

    @pytest.mark.asyncio
    async def test_battlecoin_contribution(self, setup):
        network, alice, bob = setup
        try:
            result = await self.make_and_spend_battlecoin(network, alice, bob, 500)

            assert "error" not in result

            filtered_result = list(filter(
                lambda addition:
                    (addition.amount == 501) and
                    (addition.puzzle_hash == create_battlecoin_puzzle(1000000000000, bob.puzzle_hash).get_tree_hash())
            ,result["additions"]))
            assert len(filtered_result) == 1
        finally:
            await network.close()

    @pytest.mark.asyncio
    async def test_battlecoin_completion(self, setup):
        network, alice, bob = setup
        try:
            result = await self.make_and_spend_battlecoin(network, alice, bob, 1000000000000)

            assert "error" not in result

            filtered_result = list(filter(
                lambda addition:
                    (addition.amount == 0) and
                    (addition.puzzle_hash == create_battlecoin_puzzle(1000000000000, bob.puzzle_hash).get_tree_hash())
            ,result["additions"]))
            assert len(filtered_result) == 1

            filtered_result = list(filter(
                lambda addition:
                    (addition.amount == 1000000000001) and
                    (addition.puzzle_hash == bob.puzzle_hash)
            ,result["additions"]))
            assert len(filtered_result) == 1
        finally:
            await network.close()

    @pytest.mark.asyncio
    async def test_battlecoin_stealing(self, setup):
        network, alice, bob = setup
        try:
            result = await self.make_and_spend_battlecoin(network, alice, bob, -100)
            assert 'error' in result
            assert 'GENERATOR_RUNTIME_ERROR' in result['error']
        finally:
            await network.close()