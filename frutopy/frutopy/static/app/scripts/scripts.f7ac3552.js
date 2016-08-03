"use strict";angular.module("frutopyApp",["ngAnimate","ngCookies","ngResource","ngRoute","ngSanitize","ngMaterial","ngFileUpload"]).config(["$routeProvider",function(a){a.when("/",{templateUrl:"views/main.html",controller:"MainCtrl",controllerAs:"main"}).when("/login",{templateUrl:"views/login.html",controller:"LoginCtrl",controllerAs:"login"}).when("/samples",{templateUrl:"views/samples.html",controller:"SamplesCtrl"}).otherwise({redirectTo:"/"})}]).config(["$httpProvider",function(a){a.defaults.xsrfCookieName="csrftoken",a.defaults.xsrfHeaderName="X-CSRFToken"}]).config(["$mdThemingProvider",function(a){a.theme("white"),a.theme("default").primaryPalette("red").accentPalette("amber")}]),angular.module("frutopyApp").controller("MainCtrl",["$scope","Upload","$timeout",function(a,b,c){a.uploading=!1,a.uploadDone=!1,a.uploadFile=function(d){a.uploading=!0,d.upload=b.upload({url:"/upload/",data:{file:d}}),d.upload.then(function(b){c(function(){d.result=b.data}),a.uploadDone=!0,a.uploading=!1,a.dbFile=null},function(b){b.status>0&&(a.errorMsg=b.status+": "+b.data),a.uploadDone=!1,a.uploading=!1},function(a){d.progress=Math.min(100,parseInt(100*a.loaded/a.total))})}}]),angular.module("frutopyApp").controller("SidenavCtrl",["$scope","$mdMedia","$mdDialog","$location","UserService",function(a,b,c,d,e){a.customFullscreen=b("xs")||b("sm");var f=function(d){var e=(b("sm")||b("xs"))&&a.customFullscreen;c.show({controller:"GenericDialogCtrl",templateUrl:"views/about.html",parent:angular.element(document.body),targetEvent:d,clickOutsideToClose:!0,fullscreen:e,locals:{items:{}}}),a.$watch(function(){return b("xs")||b("sm")},function(b){a.customFullscreen=b===!0})};a.display=function(a){return!(a.hideLogin&&e.isLogged()||a.loginRequired&&!e.isLogged())},a.menuEntries=[{icon:"upload",title:"Upload",description:"Upload your dataset",link:"/"},{icon:"sign-in",title:"Log In",description:"Log in as an administrator",link:"/login",hideLogin:!0},{icon:"list",title:"Samples List",description:"Manage the samples list",link:"/samples",loginRequired:!0},{icon:"sign-out",title:"Logout",description:"Close your session",loginRequired:!0,clickCallback:e.doLogout},{icon:"question-circle",title:"About",description:"About Us",clickCallback:f}],a.handleClick=function(b,c){"function"==typeof b.clickCallback?b.clickCallback(c):"string"==typeof b.link&&a.goTo(b.link)},a.goTo=function(a){d.path(a)}}]),angular.module("frutopyApp").controller("ToolbarCtrl",["$scope","$mdSidenav",function(a,b){a.openSidenav=function(){b("left").open()}}]),angular.module("frutopyApp").controller("GenericDialogCtrl",["$scope","$mdDialog","items",function(a,b,c){a.close=function(){b.cancel()};for(var d in c)c.hasOwnProperty(d)&&(a[d]=c[d])}]),angular.module("frutopyApp").controller("LoginCtrl",["$scope","$location","$mdToast","UserService",function(a,b,c,d){function e(){b.path("/samples")}d.isLogged()&&e(),a.loading=!1,a.errorMessage=null,a.email="",a.password="",a.doLogin=function(){a.loading=!0,d.doLogin(a.email,a.password).then(function(){c.show(d.getLoggedInToast()),e()},function(b){a.loading=!1,a.errorMessage=b.message})}}]),angular.module("frutopyApp").controller("SamplesCtrl",["$scope","UserService","$location","$timeout","$mdToast","$mdMedia","$mdDialog",function(a,b,c,d,e,f,g){b.isLogged()||c.path("/login"),a.loading=!1,a.labels=["Not ripe","WAT","BRUH"],a.samples=[{ID:0,fruit:"Grape",label:"Not ripe",image:"123.jpg",valid:!0},{ID:1,fruit:"Grape",label:"Not ripe",valid:!1}],a.customFullscreen=f("xs")||f("sm"),a.showImage=function(b,c){if(!b.image)return!1;var d=(f("sm")||f("xs"))&&a.customFullscreen;g.show({controller:"GenericDialogCtrl",templateUrl:"views/sample_image.html",parent:angular.element(document.body),locals:{items:{imagePath:b.image,sampleId:b.ID}},targetEvent:c,clickOutsideToClose:!0,fullscreen:d}),a.$watch(function(){return f("xs")||f("sm")},function(b){a.customFullscreen=b===!0})},a.update=function(b){console.log(b),a.loading=!0,d(function(){a.loading=!1,e.show(e.simple().theme("white").textContent("Sample "+b.ID+" correctly saved").position("top right").hideDelay(1e3))},300)}}]),angular.module("frutopyApp").service("UserService",["$window","$q","$timeout","$mdToast","$cookies",function(a,b,c,d,e){var f=a.localStorage.getItem("userToken");console.debug("User token",f),e.get("csrftoken")||(a.location.href="http://"+a.location.host+"/"),this.isLogged=function(){return null!=f},this.getLoggedInToast=function(){return d.simple().theme("white").textContent("Welcome back, user").position("top right").hideDelay(2e3)},this.doLogin=function(c,d){if(f){var e=b.defer();return e.reject("User already logged in"),e.promise}var h=b.defer();return g(c,d).then(function(b){f=b.token,a.localStorage.setItem("userToken",f),h.resolve(b.token)},function(a){h.reject(a)}),h.promise};var g=function(a,d){var e=b.defer();return c(function(){e.resolve({success:!0,token:"asdf"})},2e3),e.promise};this.doLogout=function(){if(!f){var c=b.defer();return c.reject("User not logged in"),c.promise}f=null,a.localStorage.removeItem("userToken");var d=b.defer();return h().then(function(a){d.resolve(a)},function(a){d.reject(a)}),d.promise};var h=function(){var a=b.defer();return c(function(){a.resolve({success:!0})},1e3),a.promise}}]),angular.module("frutopyApp").run(["$templateCache",function(a){a.put("views/about.html",'<md-dialog aria-label="About Us" ng-cloak> <form> <md-toolbar> <div class="md-toolbar-tools"> <h2>About Us</h2> <span flex></span> <md-button class="md-icon-button" ng-click="close()"> <md-icon md-font-icon="fa-close" style="font-size: 20px" class="fa" aria-label="Close dialog"></md-icon> </md-button> </div> </md-toolbar> <md-dialog-content> <div class="md-dialog-content"> <h2 style="margin-top: 0">very swag. so text. very word, rate me, many lorem.</h2> <p> plz doge. such word. such word. very aenean. very aenean. go full. very amet, wow! plz sit, plz text, much lorem. go layout! much full, yes master doge. i can haz doge, such word. very word, wow! many word, many word </p> <p> such word. rate me! much layout. i can haz doge, wow! need lorem. need dolor, very word, much ipsum, wow! such swag. go full. need dolor, wow! such word. txt me. very word, such swag. many word, much lorem. </p> </div> </md-dialog-content> </form> </md-dialog>'),a.put("views/login.html",'<md-progress-circular ng-if="loading" md-mode="indeterminate" class="centralLoadingSpinner" md-diameter="88"></md-progress-circular> <form name="loginForm" class="loginForm"> <md-input-container class="md-block error-message" ng-if="errorMessage"> {{errorMessage}} </md-input-container> <md-input-container class="md-block"> <label>Email</label> <input required type="email" name="email" ng-model="email" minlength="5" maxlength="100" ng-pattern="/^.+@.+\\..+$/"> <div ng-if="loginForm.email.$invalid && loginForm.email.$touched" ng-messages="loginForm.email.$error" role="alert"> <div ng-message-exp="[\'required\', \'minlength\', \'maxlength\', \'pattern\']"> This field should look like an e-mail address. </div> </div> </md-input-container> <md-input-container class="md-block"> <label>Password</label> <input required type="password" name="password" ng-model="password"> <div ng-if="loginForm.password.$invalid && loginForm.password.$touched" ng-messages="loginForm.password.$error"> <div ng-message="required">This field is required.</div> </div> </md-input-container> <md-input-container class="md-block"> <md-button ng-disabled="loginForm.$invalid || loading" ng-click="doLogin()" style="margin-left: 0" class="md-raised md-primary"> Log In </md-button> </md-input-container> </form>'),a.put("views/main.html",'<form name="uploadForm"> <input type="file" ngf-select ng-model="dbFile" name="file" accept="application/x-gzip" required ngf-model-invalid="errorFile"> <i ng-show="uploadForm.file.$error.required"><br>This field is required</i> <br> <md-button class="md-raised" ng-disabled="!uploadForm.$valid" ng-click="uploadFile(dbFile)">Submit</md-button> <h4 ng-if="uploadDone"> Your file is being processed right now </h4> </form> <br> <md-progress-linear ng-if="uploading" md-mode="determinate" value="{{dbFile.progress}}"></md-progress-linear>'),a.put("views/sample_image.html",'<md-dialog aria-label="Sample #{{sampleId}}" ng-cloak> <form> <md-toolbar> <div class="md-toolbar-tools"> <h2>Sample #{{sampleId}}</h2> <span flex></span> <md-button class="md-icon-button" ng-click="close()"> <md-icon md-font-icon="fa-close" style="font-size: 20px" class="fa" aria-label="Close dialog"></md-icon> </md-button> </div> </md-toolbar> <md-dialog-content> <div class="md-dialog-content"> <img ng-src="{{imagePath}}"> </div> </md-dialog-content> </form> </md-dialog>'),a.put("views/samples.html",'<md-progress-circular ng-if="loading" md-mode="indeterminate" class="centralLoadingSpinner" md-diameter="88"></md-progress-circular> <md-list class="samplesList"> <md-list-item class="md-1-line"> <div layout="row" style="width: 100%"> <span flex="15">ID</span> <span flex="15">Fruit</span> <span flex="15">Label</span> <span flex="40">Image</span> <span flex="15">Validate</span> </div> </md-list-item> <md-list-item class="md-1-line" ng-repeat="sample in samples"> <div layout="row" layout-align="space-around center" style="width: 100%"> <span flex="15">{{sample.ID}}</span> <span flex="15">{{sample.fruit}}</span> <span flex="15"> <md-select ng-model="sample.label" ng-change="update(sample)" class="md-accent"> <md-option ng-repeat="label in labels" value="{{label}}"> {{label}} </md-option> </md-select> </span> <span flex="40"> <md-button ng-if="sample.image" class="md-accent md-raised" ng-click="showImage(sample, $event)">Show Image</md-button> </span> <span flex="15"> <div ng-repeat="v in [0]"> <!-- See https://github.com/angular/material/issues/2819#issuecomment-136321546 --> <md-checkbox ng-change="update(sample)" ng-model="sample.valid" aria-label="Validate sample {{sample.ID}}"></md-checkbox> </div> </span> </div> </md-list-item> </md-list>')}]);