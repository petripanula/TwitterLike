import random
import traceback
import logging
from time import sleep
from twython import Twython

tweet = []
pic_tweet = []
tweet_pic = []


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

def tweet_message(message):
    message1="Tweeted: %s Length: %s" % (message, len(message))
    logging.info(message1)

    while True:
        try:
            twitter.update_status(status=message)
        except Exception as e:
            err_message = "Oops! ", e.__class__, "occurred: %s" % e
            if "ConnectionResetError" in e: 
                logging.error("We have connection problems - lets retry after sleep....")
                sleep(60)
            else:
                logging.error(err_message)
                logging.error(traceback.format_exc())
                logging.error("Next entry.")
                break
        else:
            logging.info("All good - next entry.")
            break

def tweet_message_with_pic(message,pic):
    message1="Tweeted: %s Length: %s" % (message, len(message))
    logging.info(message1)
    
    try:
        image = open(pic, 'rb')
    except Exception as e:
        err_message = "Oops! ", e.__class__, "occurred: %s" % e
        logging.error(err_message)
        logging.error(traceback.format_exc())
        logging.error("We return...")

    try:
        response = twitter.upload_media(media=image)
    except Exception as e:
        err_message = "Oops! ", e.__class__, "occurred: %s" % e
        logging.error(err_message)
        logging.error(traceback.format_exc())
        logging.error("We return...")

    media_id = [response['media_id']]

    while True:
        try:
            twitter.update_status(status=message, media_ids=media_id)
        except Exception as e:
            err_message = "Oops! ", e.__class__, "occurred: %s" % e
            if "ConnectionResetError" in e: 
                logging.error("We have connection problems - lets retry after sleep....")
                sleep(60)
            else:
                logging.error(err_message)
                logging.error(traceback.format_exc())
                logging.error("Next entry.")
                break
        else:
            logging.info("All good - next entry.")
            break
        
def tags():
    tag = []
    tag.append("#Bitcoin")
    tag.append("#cryptocurrency")
    tag.append("#XRP")
    tag.append("#WRX")
    tag.append("$cryptocurrency")
    tag.append("#blockchain")
    tag.append("#crypto")
    tag.append("#ethereum")
    tag.append("#bitcoinmining")
    tag.append("#ltc")
    tag.append("#Altcoin")
    tag.append("#ripple")
    tag.append("#market")
    tag.append("#kucoin")
    tag.append("#uniswap")
    tag.append("#rise")
    tag.append("#btc")
    tag.append("#bitcoinnews")
    tag.append("#forex")
    tag.append("#investing")
    tag.append("#investor")
    tag.append("#financialfreedom")
    tag.append("#money")
    tag.append("#ReListXRP")
    tag.append("$XRP")
    tag.append("#SupplyChain")
    tags = len(tag)
    return tag[random.randint(0,tags-1)]

def saved_pic_tweets():
    """
    pic_tweet.append("Daily chart of $TONE looks so good. Just waiting these small cap coins will explode! @TE_FOOD #Crypto")
    tweet_pic.append("images/TONEBTC.png")  #Vaihdetaa kuva jossain välissä
    """
    """
    pic_tweet.append("$TONE it's a big ecosystem,a big project. a new giant is coming into the supply chain system. KuCoin bought a bag of ddn invest in real projects for financial freedom. never invest cryptocurrencies without projects")
    tweet_pic.append("images/tone_enterprises.jpeg")
    pic_tweet.append("Learn more about the tokenomics of TE-FOOD $TONE #TONE. Based on a dual token model, we aim to provide a sustainable ecosystem for supply chains around the world. #Crypto")
    tweet_pic.append("images/dual_token.jpeg")
    pic_tweet.append("Interesting new registration options have been added TE-FOOD's TrustOne app!! #Crypto $XRP #BTC #Covid19")
    tweet_pic.append("images/trustone_app_options.jpeg")
    pic_tweet.append("When #Altseason? Dont focus on a date but understand money flow. Duration of the phases are parabolic meaning first takes longest & last goes fastest. Phases overlap & can temporarily reverse. We are in Phase 2-3 #Altseason2021 $TONE")
    tweet_pic.append("images/altseason_path.jpeg")
    pic_tweet.append("Just making it clear - TE-FOOD $TONE it's not only food related tracking company. It will cover a lot in the future - all kind of things in Supply Chain. TE-FOOD $TONE #kucoin #uniswap $BTC $ETH #supplychain #WHBT")
    tweet_pic.append("images/WBHT.jpeg")
    """
    
    pic_tweet.append("$XRP shit coin? Just take a moment and study it by yourself. #XRP is the only hi-cap alt which is not really gained value during this crypto season, but very soon new ATH. Stay tuned! #BTC #Crypto #altseason")
    tweet_pic.append("images/XRP_ekosystem.png")
    """
    pic_tweet.append("Ripple is known for its large partnerships with banks. Banks have invested and continue to invest in Ripple for many years. As you may know, the banks have a good understanding of where to invest money #XRP $XRP to $10")
    tweet_pic.append("images/XRP_investors.jpg")
    pic_tweet.append("#XRP use cases. Hate it or love it - that doesn't change the facts. #BNB #BTC $XRP #Crypto")
    tweet_pic.append("images/XRP_use_cases.jpg")
    """
    """
    pic_tweet.append("Screenshots from TE-FOOD TrustoneApp! https://www.trustoneapp.com/  95% of all Crypto projects can only dream about this kind of adaptation. $TONE #TONE #Crypto #altseason #covid19")
    tweet_pic.append("images/trustone.jpg")
    pic_tweet.append("#XRP Holders! The biggest reason we don't have more xrp millionaires after 2018 was weak hands when the price dropped several days. If you can't day trade just HODL! $XRP You thank me later! Pic from 2018")
    tweet_pic.append("images/XRP_rise_2018.png")
    """
    """
    pic_tweet.append("$VET #VeChain can you name one continent from the globe where you have partnerships? Is your market cap (15 billion) really sustainable or is $TONE serious undervalued (~50milj) $TONE http://www.supergroup.co.za/about/latest-news-article/53")
    tweet_pic.append("images/supergroup.png")
    """
def saved_tweets():
    """
    tweet.append("TrustOne's #blockchain based solution assists travelers to get tested in order to travel to or from the UK. $TONE $Crypto https://medium.com/te-food/travelling-in-the-uk-now-is-easier-with-trustone-fdcda93b6a6d")
    tweet.append("Tokenomics of TE-FOOD. Based on a dual token model, we aim to provide a sustainable ecosystem for supply chains around the world. $TONE is the basis of the tokenomics, and is required for every transaction on the TrustChain. #crypto https://twitter.com/TE_FOOD/status/1379697932010676225?s=20")
    tweet.append("Supply chain projects daily operations: \n$TONE = 403,137 \n$VET = 71,991 \n$MRPH = ?? \n$WTC = ?? \n$AMB= ?? \nCan followers of these projects provide the numbers in the replies #kucoin #uniswap $BTC $ETH) https://blocktivity.info/")
    tweet.append("TE-FOOD's partnerships (including those with GE Aviation, Auchan and Migros), none are more exciting than Supergroup of South Africa! This is the next #KuCoin 10-100x coin! $TONE #crypto #uniswap $BTC $ETH http://www.supergroup.co.za/about/latest-news-article/53")
    tweet.append("TE-FOOD has always done things differently. This will be very interesting #DeFi $TONE #kucoin #uniswap $BTC $ETH #crypto https://medium.com/te-food/what-te-food-is-working-on-march-update-6564cb1f1e18")
    tweet.append("I challenge any other project to rival this progress in Q1 $TONE #kucoin #uniswap $BTC $ETH #crypto https://twitter.com/TE_FOOD/status/1374011584410963969?s=20")
    tweet.append("Food traceability, Covid-19 testing management, and a new initiative - check out what are we focusing in 2021! $TONE #crypto #ETH #BTC https://medium.com/te-food/what-te-food-is-working-on-march-update-6564cb1f1e18")
    tweet.append("...and TE-FOOD $TONE will be taking a nice slice. #kucoin #uniswap $ETH $BTC #Crypto https://twitter.com/IFT/status/1378354094486736897?s=20")
    tweet.append("TE-FOOD $TONE #ETH #Crypto #BTC #Kucoin https://twitter.com/TE_FOOD/status/1377883617368637446?s=20")
    tweet.append("TE-FOOD + #DeFi = ? Using the TrustChain to prove asset ownership (collateral) and offering micro-loans to farmers in developing countries would mesh quite nicely #FoodTech #Sustainability $TONE #Crypto #ETH #BTC https://twitter.com/TE_FOOD/status/1374011584410963969?s=20")
    tweet.append("Want to see what real-world adoption looks like? Here you have a transaction recorded by TE-FOOD $TONE for a #covid test! Does any other project has such a transparent explorer? #Crypto #ETH #BTC #KuCoin #uniswap https://explorer.te-food.com/get_html/transaction/50708833")
    tweet.append("TE-FOOD $TONE has so many huge customers, that when another $billion company joins them, it barely gets noticed. Other projects dream about  this level of adoption. #kucoin #uniswap $BTC $ETH #Crypto https://twitter.com/TE_FOOD/status/1374659348505501696?s=20")
    tweet.append("Another giant customer added to TE-FOOD's trophy cabinet Trophy $TONE #kucoin #uniswap $BTC $ETH https://twitter.com/TE_FOOD/status/1374659348505501696?s=20")
    tweet.append("$TONE is so undervalued it's almost criminal. Get in while you can at these current levels. This is one of those projects that ends up getting listed on Binance and goes 10x+. #tone #tefood #crypto #blockchain #covid #cryptocurrency https://twitter.com/TE_FOOD/status/1377173406701953030?s=20")
    tweet.append("Check how TrustOne, TE-FOOD's blockchain based application helps local governments in Slovakia to test tens of thousands of residents during weekends. $tone #covid #bitcoin #btc $btc #cryptocurrency https://medium.com/te-food/cities-in-slovakia-use-trustone-to-test-residents-for-covid-19-5ed099e18a5e")
    tweet.append("What's the potential of TE-FOOD $TONE? By diluted  cap: \n+33% = $AMB \n+100% = $WTC \n+520% = $TRAC \n+9600% = $VET \n...and yet TE-FOOD manages more operations each day than these 4 projects combined #kucoin #uniswap $BTC $ETH")
    tweet.append("These aren't just partners but are actual paying customers, implementation partners or standard organizations!  @TE_FOOD was a sleeping giant for years and it's just a matter of time until $TONE takes off! #kucoin #uniswap #Crypto https://twitter.com/TE_FOOD/status/1371809512462684160?s=20")
    tweet.append("Food traceability market set to hit $26bn per year by 2025. Always great to see TE-FOOD #TONE mentioned in market research reports #blockchain #traceability #foodtech  @TEFOOD #kucoin #uniswap $BTC $ETH #Crypto https://www.marketsandmarkets.com/Market-Reports/food-traceability-market-103288069.html")
    tweet.append("Auchan Hungary implements TE-FOOD's #blockchain based traceability solution. After France, Portugal and Romania, it's the next country where the global retail giant launches its traceability initiative. $TONE #kucoin #uniswap #Crypto https://medium.com/te-food/auchan-hungary-supermarket-chain-implements-te-food-1fe4d1f94dd6")
    tweet.append("Check out video to see how they are adapting and improving grass based farming system with production technology from @Kiwitechltd traceability by @TE_FOOD. $TONE #kucoin #uniswap $BTC $ETH #Crypto https://www.youtube.com/watch?v=t42mOoCAjI0")
    tweet.append("Just another great announcement of expended traceability adoption from @TE_FOOD together with the retail giant @AUCHAN_France $TONE #kucoin #uniswap https://twitter.com/TE_FOOD/status/1294176783349227520?s=20")
    tweet.append("Time will come when 95% of all Crypto projects will try to find how to change the tokenomics sustainable as the current trend can't continue. Money doesn't come from anything. TE-FOOD has the solution already: https://twitter.com/TE_FOOD/status/1379697932010676225?s=20 $TONE #Crypto #safeinvestment")
    tweet.append("You can earn rewards by contributing to the $TONE liquidity pool on #uniswap! $BTC $ETH #Crypto #market https://info.uniswap.org/token/0x2ab6bb8408ca3199b8fa6c92d5b455f820af03c4")
    tweet.append("Check how Grupo Avícola Rujamar launched blockchain based traceability as an industry standard to prove the premium quality of their cage-free eggs. #TONE #Crypto #BTC https://medium.com/te-food/rujamar-joins-te-food-blockchain-762a6f4285b5")
    tweet.append("WoW - these things are just examples how the blockchain can help to verify the #quality! @SZ Süddeutsche Zeitung for featuring TE-FOOD! $TONE https://www.sueddeutsche.de/kolumne/blockchain-impact-social-impact-investing-entwicklungshilfe-kazi-yetu-1.5185663 #Crypto #tea #BTC")
    tweet.append("Restarting travel and leisure safely soon will need applications like TrustOne. #TONE @TE-FOOD #Covid19 #Covid-19 https://www.vice.com/en/article/dy854a/people-are-photoshopping-covid-test-results-to-bypass-travel-restrictions #BTC")
    tweet.append("Have you checked the Rotten from #Netflix? https://www.imdb.com/title/tt7763662/ How the blockchain could help there? @TE-FOOD has the solution already. $TONE #BTC #Crypto https://www.newfoodmagazine.com/article/129788/trends-and-challenges-2021/")
    tweet.append("The only thing $TONE is lacking is the strong crypto marketing game. But that will come naturally when a big audience notices the importance of this sector. @TE-FOOD #Crypto #ETH https://www.newfoodmagazine.com/article/129788/trends-and-challenges-2021/ https://www.imdb.com/title/tt7763662")
    tweet.append("You have never seen like this heavy undervalued gem $tone Mcap ~35m and can easily 10x! Real use case and the company has a lot of clients and it's blockchain activity is always in the top 20 last 3 years! @TE-FOOD Check: https://blocktivity.info/")
    tweet.append("@Poloniex @Binance @WazirXIndia The probably most undervalued project right now which should be listed on your exchange: $TONE @TE_FOOD")
    tweet.append("The probably most undervalued project right now IMO! Check this if you are looking for possible 100x coin: $TONE @TE_FOOD Some facts: https://blocktivity.info/ #Crypto")
    tweet.append("@TE_FOOD #SupplyChain \n- top10 blockchain in terms of transaction volume. \n- 6000+ businesses using it worldwide including Migros, GE Aviation, Deloitte, UN FAO,  Supergroup.\n- Team is combo of industry experts & experienced entrepreneurs\n-#kucoin #uniswap $TONE")
    tweet.append("Excellent reddit post on $TONE vs $VET by @AlyWan in the Telegram group. Comparing the two blockchain traceability projects side by side. Check it out! @TE_FOOD @vechainofficial https://www.reddit.com/r/CryptoCurrency/comments/mljo12/adoption_over_hype_tone/")
    tweet.append("$TONE it's a big ecosystem,a big project. a new giant is coming into the supply chain system. KuCoin bought a bag of ddn invest in real projects for financial freedom. never invest cryptocurrencies without projects #TONE $TONE #KuCoin #btc #defi @CryptoWizardd")
    tweet.append("@TE-FOOD $TONE is a bit like $VET, but with more adoption and a 400x smaller market cap - some upside potential! #kucoin #uniswap $BTC $ETH https://medium.com/@te_food")
    tweet.append("Wanna include some @Crypro's from moonshot portfolio to your bag: https://cryptoquestion.tech/moonshot-portfolio-march-2021/ My pick is #TONE (TE-FOOD) #BTC #altcoin #ALTSEASON #MoonShot")
    tweet.append("TE-FOOD (#TONE) - VeChain #VET on Steroids https://reddit.com/r/CryptoCurrency/comments/me8898/tefood_tone_vechain_on_steroids/?utm_medium=android_app&utm_source=share #ETH #XRP $TONE")
    tweet.append("If you see CMC top 100-200, there are no fundamentals behind most of the projects. Those projects can't survive long without sustainable tokenomics. Check https://twitter.com/TE_FOOD/status/1379697932010676225?s=20 $TONE Only ~35milj mcap. #kucoin #uniswap")
    tweet.append("As CEO of Binance Changpeng Zhao said:\n - Don't worry about price\n - Think about utility\n - Price follow utility\nThis is so true with $TONE https://www.reddit.com/r/CryptoCurrency/comments/mljo12/adoption_over_hype_tone/")
    tweet.append("#XRP #BTC I would not trade XRP now - just HODL or BUY. It looks like it will go to the new ATH soon. You hate or love it - doesn't matter. The world needs it: https://www.youtube.com/watch?v=23Yn5GdYpJc #Crypto")
    tweet.append("#XRP really is the revolution. World needs to swap the Jurasic old Swift system. https://www.youtube.com/watch?v=23Yn5GdYpJc #Crypto #swift")
    tweet.append("Prime XBT has expected that if Ripple able to resolve its case with the Security and Exchanges Commission (SEC), the #XRP price could rise to as high as $27 per token in 2021 for the short term, increase to $34 in 2022 and $140 in 2025 https://trading-education.com/should-you-buy-ripple $XRP")
    tweet.append("$TONE http://www.supergroup.co.za/about/latest-news-article/53 If same kind of news would came from #VeChain $VET it would go x3 even 15 Billion market cap? Something is not right here. $TONE has so bright future")
    tweet.append("All #cryptoinvestor should know this. Do not follow only Hyped coins. Follow utility - money follows utility! $TONE ($TE_FOOD) #VET #BTC $doge $safemoon https://twitter.com/TE_FOOD/status/1385131254165692417?s=20")
    """



saved_tweets()
saved_pic_tweets()

"""
tweets = len(tweet)
random_list_of_tweets = random.sample(range(tweets), tweets)

for x in random_list_of_tweets:
  print(x)
  message = tweet[x] + " " + tags()
  message = tweet[x]
  tweet_message(message)
  my_sleep = random.randint(600,900)
  msg = "Sleeping %s seconds..." % my_sleep
  logging.info(msg)
  sleep(my_sleep)
"""

pic_tweets = len(pic_tweet)
print(pic_tweets)
random_list_of_pic_tweets = random.sample(range(pic_tweets), pic_tweets)
print(random_list_of_pic_tweets)
for x in random_list_of_pic_tweets:
  print(x)
  message = pic_tweet[x] + " " + tags()
  print(message)
  tweet_message_with_pic(message,tweet_pic[x])
  my_sleep = random.randint(600,900)
  msg = "Sleeping %s seconds..." % my_sleep
  logging.info(msg)
  sleep(my_sleep)
  
logging.info("We are done!")
