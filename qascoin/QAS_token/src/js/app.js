App = {
	web3Provider: null,
	contracts: {},
	account: '0x0',
	loading: false,
	tokenPrice: 1000000000000000,
	tokensSold: 0,
	tokensAvailable: 750000,

	init: function() {
		console.log("App initialized...")
		return App.initWeb3();
	},

	initWeb3:function() {
		if (typeof web3 !== 'undefined') {
	      // If a web3 instance is already provided by Meta Mask.
	      	App.web3Provider = web3.currentProvider;
	    	web3 = new Web3(web3.currentProvider);
	    	return App.initContracts();
	    } else {
	      // Specify default instance if no web3 instance provided
	      console.log("cannot connect to the website");
	      self.errorMessage = "cannot connect to the website"; 
	    }
	},

	initContracts: function() {
		$.getJSON("QASTokenSale.json", function(QASTokenSale) {
		      App.contracts.QASTokenSale = TruffleContract(QASTokenSale);
		      App.contracts.QASTokenSale.setProvider(App.web3Provider);
		      App.contracts.QASTokenSale.deployed().then(function(QASTokenSale) {
		        console.log("QAS Token Sale Address:", QASTokenSale.address);
			});
		}).done(function() {
				$.getJSON("QASToken.json", function(QASToken) {
				      App.contracts.QASToken = TruffleContract(QASToken);
				      App.contracts.QASToken.setProvider(App.web3Provider);
				      App.contracts.QASToken.deployed().then(function(QASToken) {
				        console.log("QAS Token Address:", QASToken.address);
					});
				    App.listenForEvents();
				    return App.render();
				});
			})
	},

	// Listen for events emitted from the contract
	listenForEvents: function() {
		App.contracts.QASTokenSale.deployed().then(function(instance) {
			instance.Sell({}, {
				fromBlock: 0,
				toBlock: 'latest',
			}).watch(function(error, event) {
				console.log("event triggerred", event);
				App.render();
			})
		})
	},

	render: function() {
		if (App.loading) {
			return;
		}
		App.loading = true;

		var loader = $('#loader');
		var content = $('#content');

		loader.show();
		content.hide();

		// Load account data
		web3.eth.getCoinbase(function(err, account) {
			if(err === null) {
				App.account = account;
				$('#accountAddress').html("Your current account is: " + account);
			}
		})


		App.contracts.QASTokenSale.deployed().then(function(instance) {
			QASTokenSaleInstance = instance;
			return QASTokenSaleInstance.tokenPrice();
		}).then(function(tokenPrice) {
			App.tokenPrice = 1000000000000000; // this get some problem as it cannot refer the token price with no reason
			$('.token-price').html(web3.fromWei(App.tokenPrice, "ether"));
			return QASTokenSaleInstance.tokensSold();
		}).then(function(tokensSold) {
			App.tokensSold = tokensSold.toNumber();
			$('.tokens-sold').html(App.tokensSold);
			$('.tokens-available').html(App.tokensAvailable);

			var progressPercent = (App.tokensSold/App.tokensAvailable) * 100;
			$('#progress').css('width', progressPercent + '%');

			// Load token contract
			App.contracts.QASToken.deployed().then(function(instance) {
				QASTokenInstance = instance;
				return QASTokenInstance.balanceOf(App.account);
			}).then(function(balance){
				$('.QAS-balance').html(balance.toNumber());
				
				App.loading = false;
				loader.hide();
				content.show();
			})
		});
	},

	buyTokens: function() {
		$('#content').hide();
		$('#loader').show();
		var numberOfTokens = $('#numberOfTokens').val();
		App.contracts.QASTokenSale.deployed().then(function(instance) {
			return instance.buyTokens(numberOfTokens, {
				from: App.account,
				value: numberOfTokens * App.tokenPrice,
				gas: 500000
			});
		}).then(function(result) {
			console.log("Tokens bought...")
			$('form').trigger('reset') // reset the number of tokens in form
			// Wait for Sell event
		})
	},

	transferTokens: function() {
		$('#content').hide();
		$('#loader').show();
		console.log($('#accountsTo'));
		var accountsTo = $('#accountsTo').val();
		console.log(accountsTo);
		var transferNum = $('#transferNum').val();
		App.contracts.QASToken.deployed().then(function(instance) {
			return instance.transfer(accountsTo,transferNum,{from:App.account})
		}).then(function(result) {
			console.log("Tokens transfered...")
			$('form').trigger('reset') // reset the number of tokens in form
			// Wait for Sell event
		});
	}
}

$(function() {
	$(window).load(function(){
		App.init();
	})
});