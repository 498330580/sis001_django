(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["pages-musicDetail-musicDetail"],{"390f":function(t,i,e){"use strict";var n=e("4ea4");Object.defineProperty(i,"__esModule",{value:!0}),i.default=void 0;var a=n(e("5530")),s=n(e("9c0c")),c=n(e("e409")),u=n(e("945c")),o=e("26cb"),l={data:function(){return{listStatus:!1,collectStatus:!1,nightStatus:!1}},filters:{formatTime:function(t){return 100===t?u.default.formatTime(0):u.default.formatTime(t)}},components:{pageTitle:s.default,uniPopup:c.default},computed:(0,a.default)((0,a.default)({},(0,o.mapState)({durationTime:function(t){var i=t.audio;return i.durationTime},currentTime:function(t){var i=t.audio;return i.currentTime},audioList:function(t){var i=t.audio;return i.audioList},playStatus:function(t){var i=t.audio;return i.playStatus}})),(0,o.mapGetters)(["audioName","singerName","singerSynopsis"])),methods:(0,a.default)((0,a.default)({},(0,o.mapActions)(["PlayOrPause","PreOrNext","sliderToPlay","selectPlay"])),{},{chageStatus:function(t){this[t]=!this[t]},showSingerSynopsis:function(){this.$refs.popup.open()}})};i.default=l},"4c25":function(t,i,e){t.exports=e.p+"static/img/music1.e8b9c6ff.png"},"55a0":function(t,i,e){"use strict";e.r(i);var n=e("390f"),a=e.n(n);for(var s in n)"default"!==s&&function(t){e.d(i,t,(function(){return n[t]}))}(s);i["default"]=a.a},"73e0":function(t,i,e){"use strict";e.d(i,"b",(function(){return a})),e.d(i,"c",(function(){return s})),e.d(i,"a",(function(){return n}));var n={uniPopup:e("e409").default},a=function(){var t=this,i=t.$createElement,n=t._self._c||i;return n("v-uni-view",{class:t.nightStatus?"nightTheme":"",staticStyle:{height:"100vh"}},[n("page-title",{attrs:{Theme:t.nightStatus?"nightTheme":"bg-white"}},[t._v("音乐详情")]),n("v-uni-view",{staticClass:"d-inline-block w-100 text-center py-2"},[n("v-uni-view",[n("v-uni-text",{staticClass:"font"},[t._v("歌曲:")]),n("v-uni-text",{staticClass:"font-weight-bold"},[t._v(t._s(t.audioName))])],1),n("v-uni-view",[n("v-uni-text",{staticClass:"font"},[t._v("歌手:")]),n("v-uni-text",{staticClass:"font-weight-bold"},[t._v(t._s(t.singerName))])],1)],1),n("v-uni-view",{staticClass:"flex align-center justify-center"},[n("v-uni-image",{staticStyle:{"border-radius":"35rpx","box-shadow":"0 2rpx 6rpx 0",width:"600rpx",height:"380rpx"},attrs:{src:e("4c25"),"lazy-load":!0,mode:"aspectFill"}})],1),n("v-uni-view",{staticClass:"flex align-center justify-center font",staticStyle:{color:"#7a8388",height:"65rpx"}},[n("v-uni-view",[t._v(t._s(t._f("formatTime")(t.durationTime)))]),n("v-uni-view",{staticStyle:{width:"500rpx"}},[n("v-uni-slider",{attrs:{"block-size":"16",activeColor:"#e48267",backgroundColor:"#eef2f3",max:t.durationTime,value:t.currentTime},on:{change:function(i){arguments[0]=i=t.$handleEvent(i),t.sliderToPlay.apply(void 0,arguments)},changing:function(i){arguments[0]=i=t.$handleEvent(i),t.sliderToPlay.apply(void 0,arguments)}}})],1),n("v-uni-view",[t._v(t._s(t._f("formatTime")(t.currentTime)))])],1),n("v-uni-view",[n("v-uni-view",{staticClass:"flex align-center justify-center",staticStyle:{"padding-top":"50rpx"}},[n("v-uni-view",{staticClass:"mr-3",on:{click:function(i){arguments[0]=i=t.$handleEvent(i),t.PreOrNext("pre")}}},[n("my-icon",{attrs:{iconId:"icon-shangyixiang",iconSize:"85"}})],1),n("v-uni-view",{staticClass:"mx-5",on:{click:function(i){arguments[0]=i=t.$handleEvent(i),t.PlayOrPause.apply(void 0,arguments)}}},[n("my-icon",{attrs:{iconId:t.playStatus?"icon-zanting":"icon-bofang1",iconSize:"80"}})],1),n("v-uni-view",{staticClass:"ml-2",on:{click:function(i){arguments[0]=i=t.$handleEvent(i),t.PreOrNext("next")}}},[n("my-icon",{attrs:{iconId:"icon-xiayixiang",iconSize:"85"}})],1)],1),n("v-uni-view",{staticClass:"flex align-center justify-center font",staticStyle:{"padding-top":"50rpx"}},[n("v-uni-view",{staticClass:"flex flex-column align-center",on:{click:function(i){arguments[0]=i=t.$handleEvent(i),t.chageStatus("listStatus")}}},[n("my-icon",{attrs:{iconId:t.listStatus?"icon-liebiao":"icon-icon--",iconSize:"60"}}),n("v-uni-text",{staticClass:"pt-1"},[t._v("播放列表")])],1),n("v-uni-view",{staticClass:"flex flex-column align-center",staticStyle:{padding:"0 80rpx"},on:{click:function(i){arguments[0]=i=t.$handleEvent(i),t.chageStatus("collectStatus")}}},[n("my-icon",{attrs:{iconId:t.collectStatus?"icon-xihuan2":"icon-aixinfengxian",iconSize:"60"}}),n("v-uni-text",{staticClass:"pt-1"},[t._v("收藏")])],1),n("v-uni-view",{staticClass:"flex flex-column align-center",on:{click:function(i){arguments[0]=i=t.$handleEvent(i),t.chageStatus("nightStatus")}}},[n("my-icon",{attrs:{iconId:t.nightStatus?"icon-yueliang":"icon-yejianmoshi",iconSize:"60"}}),n("v-uni-text",{staticClass:"pt-1"},[t._v("夜间模式")])],1)],1)],1),n("v-uni-view",{directives:[{name:"show",rawName:"v-show",value:!t.listStatus,expression:"!listStatus"}],staticClass:"fixed-bottom shadow p-2 animated fadeInUp",staticStyle:{height:"260rpx","border-radius":"30rpx","z-index":"0"}},[n("v-uni-view",{staticClass:"flex justify-between"},[n("v-uni-view",[n("v-uni-view",[n("v-uni-text",{staticClass:"font"},[t._v("歌曲:")]),n("v-uni-text",{staticClass:"font-weight-bold"},[t._v(t._s(t.audioName))])],1),n("v-uni-view",[n("v-uni-text",{staticClass:"font"},[t._v("歌手:")]),n("v-uni-text",{staticClass:"font-weight-bold"},[t._v(t._s(t.singerName))])],1)],1),n("my-icon",{attrs:{iconId:"icon-jieshao",iconSize:"65"},on:{"my-click":function(i){arguments[0]=i=t.$handleEvent(i),t.showSingerSynopsis.apply(void 0,arguments)}}})],1),n("v-uni-view",[n("v-uni-view",{staticClass:"font-md pt-2"},[t._v("歌手简介:")]),n("v-uni-view",{staticClass:"text-ellipsis w-100"},[t._v(t._s(t.singerSynopsis))])],1)],1),n("v-uni-view",{directives:[{name:"show",rawName:"v-show",value:t.listStatus,expression:"listStatus"}],staticClass:"fixed-bottom shadow p-2 animated fadeInUp",staticStyle:{height:"260rpx","border-radius":"30rpx"}},[n("v-uni-view",{staticClass:"font-weight-bold font-md",staticStyle:{height:"50rpx"}},[t._v("列表选择")]),n("v-uni-scroll-view",{staticStyle:{height:"350rpx"},attrs:{"scroll-y":!0}},[t._l(t.audioList,(function(i,e){return[n("v-uni-view",{key:i.id+"_0",staticClass:"flex align-center font px-2",staticStyle:{height:"85rpx"},attrs:{"hover-class":"bg-light"},on:{click:function(e){arguments[0]=e=t.$handleEvent(e),t.selectPlay(i.id)}}},[n("v-uni-text",{staticClass:"flex-1 text-ellipsis"},[t._v(t._s(i.audioName))]),n("v-uni-text",{staticClass:"flex-1 text-ellipsis"},[t._v(t._s(i.singerName))]),n("v-uni-view",{staticClass:"flex-1 ml-3 flex align-center"})],1)]}))],2)],1),n("uni-popup",{ref:"popup"},[n("v-uni-view",{staticClass:"px-2 shadow",class:t.nightStatus?"nightTheme":"bg-white",staticStyle:{width:"600rpx",height:"850rpx","border-radius":"40rpx"}},[n("v-uni-text",{staticClass:"font"},[t._v(t._s(t.singerSynopsis))])],1)],1)],1)},s=[]},"9c0c":function(t,i,e){"use strict";e.r(i);var n=e("ec46"),a=e("b71a");for(var s in a)"default"!==s&&function(t){e.d(i,t,(function(){return a[t]}))}(s);var c,u=e("f0c5"),o=Object(u["a"])(a["default"],n["b"],n["c"],!1,null,"0213bccc",null,!1,n["a"],c);i["default"]=o.exports},b71a:function(t,i,e){"use strict";e.r(i);var n=e("e97d"),a=e.n(n);for(var s in n)"default"!==s&&function(t){e.d(i,t,(function(){return n[t]}))}(s);i["default"]=a.a},e97d:function(t,i,e){"use strict";Object.defineProperty(i,"__esModule",{value:!0}),i.default=void 0;var n={data:function(){return{statusBarHeight:this.statusBarHeight}},props:{Theme:{type:String,default:"bg-white"}},methods:{quit:function(){uni.navigateBack({delta:1})}}};i.default=n},ec46:function(t,i,e){"use strict";var n;e.d(i,"b",(function(){return a})),e.d(i,"c",(function(){return s})),e.d(i,"a",(function(){return n}));var a=function(){var t=this,i=t.$createElement,e=t._self._c||i;return e("v-uni-view",{class:t.Theme},[e("v-uni-view",{class:t.Theme,style:{height:t.statusBarHeight+"px",paddingTop:"60rpx"}}),e("v-uni-view",{staticClass:"fixed-top",class:t.Theme,style:{height:t.statusBarHeight+"px"}}),e("v-uni-view",{staticClass:"flex align-center position-fixed w-100",class:t.Theme,staticStyle:{"z-index":"99"},style:{height:"60rpx",top:t.statusBarHeight+"px"}},[e("my-icon",{staticClass:"mx-2",attrs:{iconId:"icon-jiantou-copy"},on:{"my-click":function(i){arguments[0]=i=t.$handleEvent(i),t.quit.apply(void 0,arguments)}}}),e("v-uni-view",{staticClass:"font-lg"},[t._t("default")],2)],1)],1)},s=[]},f077:function(t,i,e){"use strict";e.r(i);var n=e("73e0"),a=e("55a0");for(var s in a)"default"!==s&&function(t){e.d(i,t,(function(){return a[t]}))}(s);var c,u=e("f0c5"),o=Object(u["a"])(a["default"],n["b"],n["c"],!1,null,"6de55ec1",null,!1,n["a"],c);i["default"]=o.exports}}]);