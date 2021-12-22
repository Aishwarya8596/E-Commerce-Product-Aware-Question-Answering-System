sap.ui.define(
    ['sap/ui/core/UIComponent',
        'sap/ui/model/json/JSONModel',
        'sap/f/FlexibleColumnLayoutSemanticHelper',
        'sap/f/library'],
    /**
     * @param {typeof sap.ui.core.UIComponent} UIComponent 
     * @param {typeof sap.ui.Device} Device 
     */
    function (UIComponent, JSONModel, FlexibleColumnLayoutSemanticHelper, fioriLibrary) {
        "use strict";

        return UIComponent.extend("com.sjsu.ECommerceQnA.Component", {
            metadata: {
                manifest: "json"
            },

            /**
             * The component is initialized by UI5 automatically during the startup of the app and calls the init method once.
             * @public
             * @override
             */
            init: function () {
                var oModel,
                    oProductsModel,
                    oRouter;

                UIComponent.prototype.init.apply(this, arguments);

                oModel = new JSONModel();
                this.setModel(oModel);

                // set products demo model on this sample
                oProductsModel = new JSONModel(sap.ui.require.toUrl('com/sjsu/ECommerceQnA/mockdata/products.json'));
                oProductsModel.setSizeLimit(1000);
                this.setModel(oProductsModel, 'products');

                oRouter = this.getRouter();
                oRouter.attachBeforeRouteMatched(this._onBeforeRouteMatched, this);
                oRouter.initialize();
            },


            getHelper: function () {
                return this._getFcl().then(function (oFCL) {
                    var oSettings = {
                        defaultTwoColumnLayoutType: fioriLibrary.LayoutType.TwoColumnsMidExpanded,
                        defaultThreeColumnLayoutType: fioriLibrary.LayoutType.ThreeColumnsMidExpanded,
                        initialColumnsCount: 2
                    };
                    return (FlexibleColumnLayoutSemanticHelper.getInstanceFor(oFCL, oSettings));
                });
            },

            _onBeforeRouteMatched: function (oEvent) {
                var oModel = this.getModel(),
                    sLayout = oEvent.getParameters().arguments.layout,
                    oNextUIState;

                // If there is no layout parameter, query for the default level 0 layout (normally OneColumn)
                if (!sLayout) {
                    this.getHelper().then(function (oHelper) {
                        oNextUIState = oHelper.getNextUIState(0);
                        oModel.setProperty("/layout", oNextUIState.layout);
                    });
                    return;
                }

                oModel.setProperty("/layout", sLayout);
            },

            _getFcl: function () {
                return new Promise(function (resolve, reject) {
                    var oFCL = this.getRootControl().byId('flexibleColumnLayout');
                    if (!oFCL) {
                        this.getRootControl().attachAfterInit(function (oEvent) {
                            resolve(oEvent.getSource().byId('flexibleColumnLayout'));
                        }, this);
                        return;
                    }
                    resolve(oFCL);

                }.bind(this));
            }
        });
    }
);
