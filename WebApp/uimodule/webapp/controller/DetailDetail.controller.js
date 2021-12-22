sap.ui.define([
	"sap/ui/model/json/JSONModel",
	"sap/ui/core/mvc/Controller"
], function (JSONModel, Controller) {
	"use strict";

	return Controller.extend("com.sjsu.ECommerceQnA.controller.DetailDetail", {
		onInit: function () {
			this.oOwnerComponent = this.getOwnerComponent();

			this.oRouter = this.oOwnerComponent.getRouter();
			this.oModel = this.oOwnerComponent.getModel();

			this.oRouter.getRoute("detailDetail").attachPatternMatched(this._onPatternMatch, this);
		},

		handleAboutPress: function () {
			var oNextUIState;
			this.oOwnerComponent.getHelper().then(function (oHelper) {
				oNextUIState = oHelper.getNextUIState(3);
				this.oRouter.navTo("page2", { layout: oNextUIState.layout });
			}.bind(this));
		},

		_onPatternMatch: function (oEvent) {
			var that = this;
			this._supplier = oEvent.getParameter("arguments").supplier || this._supplier || "0";
			this._product = oEvent.getParameter("arguments").product || this._product || "0";

			// this.getView().bindElement({
			// 	path: "/ProductCollectionStats/Filters/1/values/" + this._supplier,
			// 	model: "products"
			// });

			this.getView().byId("iptQuestion").setValue("");

			this.answersModel = new sap.ui.model.json.JSONModel();
			var respObj = { answers: [] };
			this.answersModel.setData(respObj);

			var amswersTable = this.getView().byId("idAnswersTable");
			amswersTable.setModel(this.answersModel);

			var data = this.oOwnerComponent.getModel("products").getData();
			this.reviewText = "";
			data.products[this._product].reviews.forEach(function (review) {
				that.reviewText += review.reviewText;
			});
		},

		handleFullScreen: function () {
			var sNextLayout = this.oModel.getProperty("/actionButtonsInfo/endColumn/fullScreen");
			this.oRouter.navTo("detailDetail", { layout: sNextLayout, product: this._product, supplier: this._supplier });
		},

		handleExitFullScreen: function () {
			var sNextLayout = this.oModel.getProperty("/actionButtonsInfo/endColumn/exitFullScreen");
			this.oRouter.navTo("detailDetail", { layout: sNextLayout, product: this._product, supplier: this._supplier });
		},

		handleClose: function () {
			var sNextLayout = this.oModel.getProperty("/actionButtonsInfo/endColumn/closeColumn");
			this.oRouter.navTo("detail", { layout: sNextLayout, product: this._product });
		},

		onExit: function () {
			this.oRouter.getRoute("detailDetail").detachPatternMatched(this._onPatternMatch, this);
		},

		onSubmit: function () {
			var that = this;
			sap.ui.core.BusyIndicator.show();

			var qn = this.getView().byId("iptQuestion").getValue();

			var answersList = [];
			var respObj = { answers: answersList };
			this.answersModel.setData(respObj);

			var amswersTable = this.getView().byId("idAnswersTable");
			amswersTable.setModel(this.answersModel);

			var updateTable = function (data) {
				answersList.push(data);
				that.answersModel.refresh();
				sap.ui.core.BusyIndicator.hide();
			};

			var apiUrl = "http://127.0.0.1:8000/qna/";
			var fullreview = this.reviewText;
			var trucatedreview = this.reviewText.substring(0, 511);

			var qadata1 = {
				"question": qn,
				"model": "DistilBERT",
				"reviews": trucatedreview,
			};

			$.ajax({
				type: "POST",
				url: apiUrl,
				data: JSON.stringify(qadata1),
				success: function (resp) {
					updateTable(resp);
				},
				dataType: "json",
				contentType: "application/json",
			});

			var qadata2 = {
				"question": qn,
				"model": "Longformer",
				"reviews": fullreview,
			};

			$.ajax({
				type: "POST",
				url: apiUrl,
				data: JSON.stringify(qadata2),
				success: function (resp) {
					updateTable(resp);
				},
				dataType: "json",
				contentType: "application/json",
			});

			var qadata3 = {
				"question": qn,
				"model": "RoBERTa",
				"reviews": trucatedreview,
			};

			$.ajax({
				type: "POST",
				url: apiUrl,
				data: JSON.stringify(qadata3),
				success: function (resp) {
					updateTable(resp);
				},
				dataType: "json",
				contentType: "application/json",
			});

			var qadata5 = {
				"question": qn,
				"model": "Unsupervised",
				"reviews": fullreview,
			};

			$.ajax({
				type: "POST",
				url: apiUrl,
				data: JSON.stringify(qadata5),
				success: function (resp) {
					updateTable(resp);
				},
				dataType: "json",
				contentType: "application/json",
			});

			var qadata6 = {
				"question": qn,
				"model": "Bertlarge",
				"reviews": trucatedreview,
			};

			$.ajax({
				type: "POST",
				url: apiUrl,
				data: JSON.stringify(qadata6),
				success: function (resp) {
					updateTable(resp);
				},
				dataType: "json",
				contentType: "application/json",
			});

		}
	});
});
