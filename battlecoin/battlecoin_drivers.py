from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.blockchain_format.program import Program
from chia.types.condition_opcodes import ConditionOpcode
from chia.util.ints import uint64
from chia.util.hash import std_hash

from clvm.casts import int_to_bytes

from cdv.util.load_clvm import load_clvm

BATTLECOIN_MOD = load_clvm("battlecoin.clsp","battlecoin")

# Create a battlecoin
def create_battlecoin_puzzle(amount, cash_out_puzhash):
    return BATTLECOIN_MOD.curry(amount, cash_out_puzhash)

# Generate a solution to contribute to a battlecoin
def solution_for_battlecoin(pb_coin, contribution_amount):
    return Program.to([pb_coin.amount, (pb_coin.amount + contribution_amount), pb_coin.puzzle_hash])

# Return the condition to assert the announcement
def battlecoin_announcement_assertion(pb_coin, contribution_amount):
    return [ConditionOpcode.ASSERT_COIN_ANNOUNCEMENT, std_hash(pb_coin.name() + int_to_bytes((pb_coin.amount + contribution_amount)))]
