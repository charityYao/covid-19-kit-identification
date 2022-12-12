// index.js
// 获取应用实例
const app = getApp()

Page({
  data: {
    historyStorage:[],
    tempFilePath1:'',
    tempFilePath2:'',
    s_num:0,
    v_num:0
  },
  onLoad() {
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      })
    }
  },
  chooseimage: function (e) {
    var type=e.target.dataset.sourcetype
    var _this = this;
    wx.chooseImage({
      count: 1, // 默认9
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      // sourceType: ['album', 'camera'],
      sourceType: [type], // 可以指定来源是相册还是相机，默认二者都有
      success: function (res) {
        const tempFilePath = res.tempFilePaths[0]
        _this.setData({
            tempFilePath1: tempFilePath
        })
        console.log(tempFilePath) 
      }
    })
  },
  check: function() {
    console.log("aaaaa") 
    var _this = this;
    var tempFilePath = _this.data.tempFilePath1
    console.log(tempFilePath)
    wx.uploadFile({
      url: "http://localhost:8082/model",
      filePath: tempFilePath,
      name: 'image',
      header: { "Content-Type": "multipart/form-data" },
      success:function(res){
        // const tempFilePath = wx.getStorageSync('tempFilePaths');
        // console.log(tempFilePath)
        console.log("bbbb")
        var data = JSON.parse(res.data)//转换为对象
        console.log(data)
        var detectImg=data.editimg
        _this.setData({
          tempFilePath2:detectImg,
          s_num:data.s_num,
          v_num:data.v_num
        });
        var history=wx.getStorageSync('history')
        if(history==''){
          var historyStorage=_this.data.historyStorage
          historyStorage.push(data)
          wx.setStorageSync('history',historyStorage)
        }else{
          history.push(data)
          history.reverse()
          wx.setStorageSync('history',history)
        }                         
      }
    })
  }, 
  error(e) {
    console.log(e.detail)
  }
})
