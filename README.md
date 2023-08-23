# <img src="https://altcoinsbox.com/wp-content/uploads/2023/02/base-logo-in-blue.png" width="25"> Base AI Analyst

[![Open in Colab](https://camo.githubusercontent.com/84f0493939e0c4de4e6dbe113251b4bfb5353e57134ffd9fcab6b8714514d4d1/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/drive/1OA6MSpQeDFSRM7zbxkwM0-GNoKMywv1G?usp=sharing)
![GitHub Codespaces](https://img.shields.io/badge/GitHub_Codespaces-%23121011.svg?stylee&logo=github&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991.svg?stylee&logo=OpenAI&logoColor=white)
[![Code style: black](https://img.shields.io/badge/Code%20style-black-000000.svg)](https://github.com/psf/black)

App link: https://base-ai.streamlit.app/

## TLDR
Query Base blockchain data -> Create charts on the results.

## Components
1. **Fine tuned an OpenAI model** writes SQL queries to analyze Base blockchain data.
    * [Base](https://base.org/) blockchain data provided by [Flipside](https://flipsidecrypto.xyz/).
    * Queries were sourced from Base/Flipside dashboards by [@adriaparcerisas](https://flipsidecrypto.xyz/adriaparcerisas/base-active-users-fBkhsx), [@AliTslm](https://flipsidecrypto.xyz/alitaslimi/base-mainnet-base-mainnet-s0oITj), [@jackguy](https://flipsidecrypto.xyz/jackguy/base-onchain-summer-nft-dashboard-base-onchain-summer-nft-dashboard-VfYxS8), [@piper](https://flipsidecrypto.xyz/piper/base-onchain-summer-starts-08-09-23-base---onchain-summer-starts-08.09.23-pI8o4d), and [@saeedmzn](https://flipsidecrypto.xyz/saeedmzn/base-rank-check-base-rank-check-6DQsjX).
2. **Simple [Streamlit](https://streamlit.io/) app** runs the queries against the Flipside API, then allows users to create Plotly charts on the results.
