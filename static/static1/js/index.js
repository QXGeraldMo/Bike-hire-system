"use strict";function consumData(t){if(t&&t.length>0){var e=$("#save-entry"),n="";t.forEach(function(t){n+='<div class="duty-item duty-times">\n      <div class="duty-item-top">\n      <div class="duty-item-number">'+t.dataStr+'</div>\n      <div class="duty-item-sub">'+t.unit+'</div>\n      </div>\n      <div class="duty-item-desc">'+t.content+"</div>\n      </div>"}),e.html(n)}}$(function(){$(".preview").click(function(){var t=$(this).attr("data-src");$("#source").attr("src",t),$("#video-container").css("opacity",1).css("display","flex"),document.getElementById("videoone").load(),document.getElementById("videoone").play()}),$("#closeVideo").click(function(){document.getElementById("videoone").pause(),$("#video-container").css("opacity",0),setTimeout(function(){$("#video-container").css("display"," none")},500)})}),$(document).ready(function(){window.TianQi.UBT.pageView({pageId:"PCofficialwebsite",categoryId:"platform",businessInfo:{}})}),window.onbeforeunload=function(){window.TianQi.UBT.pageViewOut({pageId:"PCofficialwebsite",categoryId:"platform",businessInfo:{}})},function(){$.ajax({url:window.API_HOST+"?website.getEnergySaveInfo",contentType:"application/json; charset=utf-8",data:JSON.stringify({action:"website.getEnergySaveInfo"}),headers:{"Content-Type":"text/plain;charset=utf-8"},type:"post",dataType:"json"}).done(function(t){var e=(t.data||[]).sort(function(t,e){return Number(t.titleNum)-Number(e.titleNum)});localStorage.setItem("save",JSON.stringify(e)),consumData(e)}).fail(function(){var t=localStorage.getItem("save");t&&consumData(JSON.parse(t))})}();