- BattleCoin is a suite of decentralized games (gamefi) on the Chia blockchain

- Players battle each other and win or lose their coins to each other

- The first game is a simple rock/paper/scissors. Alice creates a coin with a certain amount and a chosen item. Bob can contribute an equal amount and chose its own item. By following the rules of rock/paper/scissors, either Alice or Bob get the full amount or they both get refunded in case of a draw.

- More games will be added to the suite in the coming months (tic tac toe, battleship, etc.)

- Most of the logic is contained in “battlecoin.clsp”

- Battlecoin is a POC that has little to no security. In rock/paper/scissors, the second player could use a blockchain explorer to look at the item chosen by the first player to beat him every time. A future solution could be to use the hash of the item+random salt. (Also this will not be an issue with tic tac toe and similar future games that do not rely on chance but purely on strategy)
