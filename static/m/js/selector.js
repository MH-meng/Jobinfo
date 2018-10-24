var JSLOADED = [],
        evalscripts = [];
function appendscript(src, text, reload, charset) {
    var id = hash(src + text);
    if (!reload && in_array(id, evalscripts)) {
        return
    }
    if (reload && $(id)) {
        $(id).parentNode.removeChild($(id))
    }
    evalscripts.push(id);
    var scriptNode = document.createElement("script");
    scriptNode.type = "text/javascript";
    scriptNode.id = id;
    scriptNode.charset = 'utf-8';
    try {
        if (src) {
            scriptNode.src = src;
            scriptNode.onloadDone = false;
            scriptNode.onload = function () {
                scriptNode.onloadDone = true;
                JSLOADED[src] = 1
            };
            scriptNode.onreadystatechange = function () {
                if ((scriptNode.readyState == "loaded" || scriptNode.readyState == "complete") && !scriptNode.onloadDone) {
                    scriptNode.onloadDone = true;
                    JSLOADED[src] = 1
                }
            }
        } else {
            if (text) {
                scriptNode.text = text
            }
        }
        document.getElementsByTagName("head")[0].appendChild(scriptNode)
    } catch (e) {
    }
}
function stripscript(s) {
    return s.replace(/<script.*?>.*?<\/script>/ig, "")
}
function hash(string, length) {
    var length = length ? length : 32;
    var start = 0;
    var i = 0;
    var result = "";
    filllen = length - string.length % length;
    for (i = 0; i < filllen; i++) {
        string += "0";
    }
    while (start < string.length) {
        result = stringxor(result, string.substr(start, length));
        start += length;
    }
    return result;
}
function stringxor(s1, s2) {
    var s = "";
    var hash = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    var max = Math.max(s1.length, s2.length);
    for (var i = 0; i < max; i++) {
        var k = s1.charCodeAt(i) ^ s2.charCodeAt(i);
        s += hash.charAt(k % 52)
    }
    return s
}
function in_array(needle, haystack) {
    if (typeof needle == "string" || typeof needle == "number") {
        for (var i in haystack) {
            if (haystack[i] == needle) {
                return true;
            }
        }
    }
    return false;
}
function str2arr(str, level, key) {
    var key = key || ''; key+='';
    var temp_str = key.substr(2);
    if (temp_str == "0000")
    {
        var temp_str1 = key.substr(0, 2);
        r = new RegExp("@(" + temp_str1 + "[^#]*)#([^@]+)", "gi"),
                arr = [], len = 6;
    } else
    {
        var key = key || '',
                r = new RegExp("@(" + key + "[^#]*)#([^@]+)", "gi"),
                arr = [], len = level * 3;
    }
    str.replace(r, function (a, x, y) {
        if (((level == 1 && x.length <= len) || (level != 1 && x.length == len)) || x === '0' && level == 1)
        {
            var temp_x = x.substr(2);
            if (x == key && temp_x == "0000")
            {
                //arr.push([x, y]);
            } else
            {
                arr.push([x, y]);
            }

        }
        var temp_x = x.substr(2);
        if (temp_x == "0000" && level == 1)
        {
            arr.push([x, y]);
        }
        return '';
    });
    return arr;
}
function thearr(str, key) {
    var r = new RegExp("@" + key + "#([^@]+)@", "gi");
    var m = str.match(r);
    m = m[0].split('#');
    m = m[1].split('@');
    return m[0];
}

(function ($) {
    $.fn.extend({
        MySelector: function (opt) {
            var setting = $.extend({
                Max: 3,
                js: "DataIndustry",
                title: "项目",
                type: 1, //1，二级
                defaultValueTitle: null,
                cacheTime: '',
                english: 0,
                standrad: 0,
                ok: function () {
                    $.noop();
                },
                cancel: function () {
                    $.noop();
                }
            },
            opt);
            var check = false;
            var onlyOne = setting.Max == 1 ? true : false;
            var the = this;
            var cache = {};
            function updateSelect() {
                $("#selector-lv2 .lv1").removeClass("sel");
                if (setting.js == "DataDistrictnew")
                {
//                    $.each($("#selector-selected span"),
//                            function(k, v) {
//                                var id = v.id.split("selectedItem_")[1];
//                                $("#item_" + id.substr(0, 2)).addClass("sel")
//                            })
                } else
                {
                    $.each($("#selector-selected span"),
                            function (k, v) {
                                var id = v.id.split("selectedItem_")[1];
                                $("#item_" + id.substr(0, 3)).addClass("sel")
                            })
                }

            }
            function _initSelector() {
                //判断js是否是object
                if (typeof setting.js == 'object') {
                    cache = setting.js;
                    if (setting.standrad)
                        selectorStandrad(true);
                    else
                        selectorType1(true);
                } else {
                    var run = function () {
                        eval("check = typeof cache_" + setting.js + " == 'string'");
                        if (check) {
                            eval("cache=cache_" + setting.js);
                            if (setting.defaultValueTitle != null) {
                                cache = $.extend(setting.defaultValueTitle, cache);
                            }
                            eval('selectorType' + setting.type + '();');
                        } else {
                            setTimeout(function () {
                                checkrun();
                            },
                                    50);
                        }
                    };
                    var checkrun = function () {
                        if (JSLOADED[src]) {
                            run();
                        } else {
                            setTimeout(function () {
                                checkrun();
                            },
                                    50);

                        }
                    };
                    var pre = "cache_";
                    src = JSPATH + pre + setting.js + ".js?" + setting.cacheTime;
                    if (!JSLOADED[src]) {
                        appendscript(src)
                    }
                    checkrun();
                }
            }
            function selectorType1(json) {

                var html = '<div id="selector-wrap" id="selector-wrap">';
                html += '<dl id="selector-selected-wrap" class="cl">';
                html += "<dt>已选择的" + setting.title + "：</dt>";
                html += '<dd class="cl"><div id="selector-selected"></div></dd>';
                html += "</dl>";
                html += '<div id="selector-options-wrap">';
                html += '<div id="selector-lv1">';
                var json = json || false;
                if (json) {
                    for (var i in cache) {
                        html += '<span id="item_' + i + '" class="s">' + cache[i] + "</span>"
                    }
                } else {
                    var v1arr = str2arr(cache, 1);
                    for (var i in v1arr) {
                        html += '<span id="item_' + v1arr[i][0] + '" class="s">' + v1arr[i][1] + "</span>"
                    }
                }
                //alert(v1arr);
                html += "</div></div></div>";
                $.dialog({
                    id: "KDf435",
                    title: "请选择" + setting.title + "[本项" + (onlyOne ? "单选" : ("多选，最多选择" + setting.Max + "个")) + "]",
                    content: html,
                    fixed: false,
                    cancelVal: "关闭",
                    resize: false,
                    lock: true,
                    height: 10,
                    ok: function () {
                        var theValue = _setValue();
                        $("i", the).html(theValue[0]);
                        $("input", the).val(theValue[1]);
                        setting.ok(theValue, the);
                    },
                    cancel: function () {
                        setting.cancel();
                    },
                    init: function () {
                        initSelectType1(json);
                    }
                })

            }
            function _setValue() {
                var itemText = new Array();
                var itemValue = new Array();
                $("#selector-selected span").each(function (k, v) {
                    itemText[k] = $(v).text();
                    itemValue[k] = v.id.split("selectedItem_")[1]
                });
                var text = itemText.join();
                var value = itemValue.join();
                return [text, value]
            }
            function defaultSelect(type, json) {
                var json = json || false;
                if ($("input", the).val()) {
                    var seled = $("input", the).val().split(",");
                    var k = 0;
                    var html = "";
                    for (var i in seled) {
                        $("#item_" + seled[i]).addClass("click");
                        if (json)
                            var name = cache[seled[i]];
                        else
                            var name = thearr(cache, seled[i]);
                        html += '<span id="selectedItem_' + seled[i] + '">' + name + "</span>";
                        k++
                    }
                    $("#selector-selected").html(html)
                }
            }
            function initSelectType1(json) {
                $("#selector-options-wrap").off('click', '.s').on('click', '.s', function () {
                    var t = $(this);
                    var id = this.id.split("item_")[1];
                    if ($(this).hasClass("click")) {
                        $(this).removeClass("click");
                        $("#selectedItem_" + id).remove()
                    } else {
                        var html = '<span id="selectedItem_' + id + '" href="javascript:;">' + $(this).text() + "</span>";
                        if (onlyOne) {
                            t.addClass("click").siblings().removeClass("click");
                            $("#selector-selected").html(html)
                        } else {
                            if ($("#selector-selected span").length >= setting.Max) {
                                $.dialog({
                                    icon: "error",
                                    content: "最多选择" + setting.Max + "个哦",
                                    lock: true
                                })
                            } else {
                                t.addClass("click");
                                $("#selector-wrap #selector-selected").append(html)
                            }
                        }
                    }
                });
                $("#selector-selected").off('click', 'span').on("click", 'span',
                        function () {
                            var id = this.id.split("selectedItem_")[1];
                            $(this).remove();
                            $("#item_" + id).removeClass("click")
                        });
                defaultSelect(1, json);
            }
            function selectorType2() {
                var html = '<div id="selector-wrap" id="selector-wrap">';
                html += '<dl id="selector-selected-wrap" class="cl">';
                html += "<dt>已选择的" + setting.title + "：</dt>";
                html += '<dd id="selector-selected" class="cl"></dd>';
                html += "</dl>";
                html += '<div id="selector-options-wrap">';
                html += '<div id="selector-lv2" class="cl">';


                var v1arr = str2arr(cache, 1);
                //alert(v1arr);
                for (var i in v1arr) {
                    html += '<span class="lv1" id="item_' + v1arr[i][0] + '"><b></b><i>' + v1arr[i][1] + "</i></span>"
                }
                html += "</div></div></div>";
                $.dialog({
                    title: "请选择" + setting.title + "[本项" + (onlyOne ? "单选" : ("多选，最多选择" + setting.Max + "个,点击" + setting.title + "可进行二级选择")) + "]",
                    content: html,
                    fixed: true,
                    cancelVal: "关闭",
                    resize: false,
                    lock: true,
                    ok: function () {
                        var theValue = _setValue();
                        $("i", the).html(theValue[0]);
                        $("input", the).val(theValue[1]);
                        setting.ok(theValue, the);
                    },
                    cancel: function () {
                        setting.cancel();
                    },
                    init: function () {
                        initSelectType2();
                    }
                })
            }
            function initSelectType2() {

                //点击选择一级分类
                $("#selector-lv2 b").click(function () {
                    var t = $(this);
                    var that = $(this).parent();
                    var id = that.attr("id").split("item_")[1];
                    if (that.hasClass("click")) {
                        that.removeClass("click");
                        $("#selectedItem_" + id).remove();
                        $("#children_" + id + " span").removeClass("click")
                    } else {
                        var ids = new Array();
                        var k = 0;

                        var v2arr = str2arr(cache, 2, id);
                        for (var i in v2arr) {
                            ids[k] = "#selectedItem_" + v2arr[i][0];
                            k++
                        }
                        $(ids.join()).remove();
                        var html = '<span id="selectedItem_' + id + '">' + that.text() + "</span>";
                        if (onlyOne) {
                            $("#selector-lv2 .layer2 span").removeClass("click");
                            $("#selector-lv2 .lv1").removeClass("click");
                            that.addClass("click");
                            $("#selector-selected").html(html)
                        } else {
                            if ($("#selector-selected span").length >= setting.Max) {
                                $.dialog({
                                    icon: "error",
                                    content: "最多选择" + setting.Max + "个哦",
                                    lock: true
                                })
                            } else {
                                that.addClass("click");
                                $("#selector-wrap #selector-selected").append(html);
                                $("#children_" + id + " span").addClass("click")
                            }
                        }
                    }
                    updateSelect();
                })

                $("#selector-lv2 i").click(function () {
                    var that = $(this).parent();
                    var id = that.attr("id").split("item_")[1];
                    var v2arr = str2arr(cache, 2, id);
                    var className = "";
                    var isClick = that.hasClass("click");
                    if (isClick) {
                        className = "click ";
                    }


                    var className2 = v2arr.length ? 'cur' : 'nur';

                    that.addClass(className2).siblings().removeClass('cur').removeClass('nur');


                    if (!v2arr.length) {
                        var html = '<div id="layer2" class="layer2 layer2none"></div>';
                    } else {
                        var html = '<div  class="layer2 cl" id="children_' + id + '">';
                        for (var i in v2arr) {
                            theClassName = "";
                            if ($("#selectedItem_" + v2arr[i][0]).length > 0) {
                                theClassName = "click";
                            }
                            html += '<span id="item_' + v2arr[i][0] + '" class="lv2 ' + className + theClassName + '">' + v2arr[i][1] + "</span>"
                        }
                        html += "</div>";
                    }



                    $("#selector-lv2 .layer2").remove();
                    var a = that.index();
                    var d = a + (4 - (a + 1) % 4) % 4;
                    if (d >= $("#selector-lv2 .lv1").length) {
                        $("#selector-lv2").append(html)
                    } else {
                        $("#selector-lv2 .lv1:eq(" + d + ")").after(html)
                    }
                });

                $('#selector-lv2').off("click", ".lv2").on("click", ".lv2", function () {
                    var id = this.id.split("item_")[1];
                    var that = $(this).parent();
                    var t = $(this);



                    if ($("#item_" + id.substr(0, 3)).hasClass("click")) {
                        return false
                    } else {
                        if ($(this).hasClass("click")) {
                            $(this).removeClass("click");
                            $("#selectedItem_" + id).remove()
                        } else {
                            var html = '<span id="selectedItem_' + id + '">' + t.text() + "</span>";
                            if (onlyOne) {
                                $("#selector-lv2 .layer2 span").removeClass("click");
                                $("#selector-lv2 .lv1").removeClass("click");
                                t.addClass("click");
                                $("#selector-selected").html(html)
                            } else {
                                if ($("#selector-selected span").length >= setting.Max) {
                                    $.dialog({
                                        icon: "error",
                                        content: "最多选择" + setting.Max + "个哦",
                                        lock: true
                                    })
                                } else {
                                    t.addClass("click");
                                    $("#selector-selected").append(html)
                                }
                            }
                        }
                    }
                    updateSelect();
                });

                $("#selector-selected").off("click", "span").on("click", "span", function () {
                    var id = this.id.split("selectedItem_")[1];
                    $(this).remove();
                    $("#item_" + id).removeClass("click");
                    $("#children_" + id + " span").removeClass("click");
                    updateSelect();
                });
                defaultSelect(2);
                updateSelect();
            }

            function selectorType3() {
                var dialogTitle = selectTitle = '';
                if (setting.english == 0) {
                    dialogTitle = "请选择" + setting.title + "[本项" + (onlyOne ? "单选" : ("多选，最多选择" + setting.Max + "个")) + "]";
                    selectTitle = "已选择的" + setting.title;
                } else {
                    dialogTitle = setting.title + '[Select up to ' + setting.Max + ']';
                    selectTitle = "selected";
                }

                var html = '<div id="selector-wrap" id="selector-wrap">';
                html += '<dl id="selector-selected-wrap" class="cl">';
                html += "<dt>" + selectTitle + "：</dt>";
                html += '<dd class="cl"><div id="selector-selected"></div></dd>';
                html += "</dl>";
                html += '<div id="selector-options-wrap">';
                html += '<div id="selector-lv3-wrap">';
                html += '<div id="selector-lv3">';

                var hot = cache.match(/HOT=[^@]*@/);
                var hotStr = hot[0].substring(4, hot[0].length - 1);
                var hotArr = hotStr.split(',');
                for (var i in hotArr) {
                    html += '<h3>' + thearr(cache, hotArr[i]) + '</h3>';
                    html += '<ul class="cl">';
                    var v2arr = str2arr(cache, 2, hotArr[i]);
                    for (var j in v2arr) {
                        html += '<li id="item_' + v2arr[j][0] + '"  class="s ">' + v2arr[j][1] + '</li>';
                    }
                    html += '</ul>';
                }
                html += '</div>';
                html += '<div id="selector-lv3-ex" class="cl">';
                var v1arr = str2arr(cache, 1);
                for (var i in v1arr) {
                    if ((hotStr + ',').indexOf(v1arr[i][0] + ',') == '-1') {
                        html += '<span id="item_' + v1arr[i][0] + '" class="lv1">' + v1arr[i][1] + '</span>';
                    }
                }
                html += '</div>';
                html += '</div>';
                html += '</div>';
                html += '</div>';

                $.dialog({
                    id: "KDf435",
                    title: dialogTitle,
                    content: html,
                    fixed: true,
                    cancelVal: "关闭",
                    resize: false,
                    lock: true,
                    ok: function () {
                        var theValue = _setValue();
                        //console.log(theValue);
//                        $("i", the).html(theValue[0]);
//                        $("input", the).val(theValue[1]);
                        setting.ok(theValue, the);
                    },
//                    cancel: function(){
//						setting.cancel();
//					},
                    init: function () {
                        initSelectType3();
                    }
                })

            }
            function initSelectType3() {
                initSelectType1();
                $("#selector-lv3-ex .lv1").click(function () {
                    var that = $(this);
                    var id = this.id.split("item_")[1];
                    var v2arr = str2arr(cache, 2, id);
                    var className = "";
                    var isClick = that.hasClass("click");
                    if (isClick) {
                        className = "click "
                    }


                    var className2 = v2arr.length ? 'cur' : 'nur';

                    that.addClass(className2).siblings().removeClass('cur').removeClass('nur');


                    if (!v2arr.length) {
                        var html = '<div id="layer2" class="layer2 layer2none"></div>';
                    } else {
                        var html = '<div  class="layer2 cl" id="children_' + id + '">';
                        for (var i in v2arr) {
                            theClassName = "";
                            if ($("#selectedItem_" + v2arr[i][0]).length > 0) {
                                theClassName = " click"
                            }
                            html += '<span id="item_' + v2arr[i][0] + '" class="lv2 s' + className + theClassName + '">' + v2arr[i][1] + "</span>"
                        }
                        html += "</div>";
                    }



                    $("#selector-lv3-ex .layer2").remove();
                    var a = that.index();
                    var d = a + (4 - (a + 1) % 4) % 4;
                    if (d >= $("#selector-lv3-ex .lv1").length) {
                        $("#selector-lv3-ex").append(html)
                    } else {
                        $("#selector-lv3-ex .lv1:eq(" + d + ")").after(html)
                    }
                });
            }

            function selectorStandrad(json) {
                var html = '<div id="selector-wrap" id="selector-wrap">';
                html += '<dl id="selector-selected-wrap" class="cl">';
                html += "<dt>已选择的" + setting.title + "：</dt>";
                html += '<dd id="selector-selected" class="cl"></dd>';
                html += "</dl>";
                html += '<div id="selector-options-wrap">';
                html += '<div id="selector-lv2" class="cl">';

                for (var i in cache) {
                    html += '<span class="lv1" id="item_' + i + '"><b></b><i>' + cache[i]['name'] + "</i></span>"
                }
                html += "</div></div></div>";

                $.dialog({
                    title: "请选择" + setting.title + "[本项" + (onlyOne ? "单选" : ("多选，最多选择" + setting.Max + "个,点击" + setting.title + "可进行二级选择")) + "]",
                    content: html,
                    fixed: true,
                    cancelVal: "关闭",
                    resize: false,
                    lock: true,
                    ok: function () {
                        var theValue = _setValue();
                        $("i", the).html(theValue[0]);
                        $("input", the).val(theValue[1]);
                        setting.ok(theValue, the);
                    },
                    cancel: function () {
                        setting.cancel();
                    },
                    init: function () {
                        initSelectStandrad();
                    }
                })
            }
            function initSelectStandrad() {

                //点击选择一级分类
                $("#selector-lv2 b").click(function () {
                    var t = $(this);
                    var that = $(this).parent();
                    var id = that.attr("id").split("item_")[1];

                    if (that.hasClass("click")) {
                        that.removeClass("click");
                        $("#selectedItem_" + id).remove();
                        $("#children_" + id + " span").removeClass("click")
                    } else {
                        var ids = new Array();
                        var k = 0;
                        for (var i in cache[id]['children']) {
                            ids[k] = "#selectedItem_" + i;
                            k++;
                        }

                        $(ids.join()).remove();
                        var html = '<span id="selectedItem_' + id + '">' + that.text() + "</span>";
                        if (onlyOne) {
                            $("#selector-lv2 .layer2 span").removeClass("click");
                            $("#selector-lv2 .lv1").removeClass("click");
                            that.addClass("click");
                            $("#selector-selected").html(html)
                        } else {
                            if ($("#selector-selected span").length >= setting.Max) {
                                $.dialog({
                                    icon: "error",
                                    content: "最多选择" + setting.Max + "个哦",
                                    lock: true
                                })
                            } else {
                                that.addClass("click");
                                $("#selector-wrap #selector-selected").append(html);
                                $("#children_" + id + " span").addClass("click");
                            }
                        }
                    }
                    updateSelect();
                })

                $("#selector-lv2 i").click(function () {
                    var that = $(this).parent();
                    var id = that.attr("id").split("item_")[1];
//                    var v2arr = cache[id]['children'];
                    var v2arr = [];
                    for (var i in cache[id]['children']) {
                        v2arr.push([i, cache[id]['children'][i]]);
                    }
                    var className = "";
                    var isClick = that.hasClass("click");

                    if (isClick) {
                        className = "click "
                    }

                    var className2 = v2arr.length ? 'cur' : 'nur';

                    that.addClass(className2).siblings().removeClass('cur').removeClass('nur');


                    if (!v2arr.length) {
                        var html = '<div id="layer2" class="layer2 layer2none"></div>';
                    } else {
                        var html = '<div  class="layer2 cl" id="children_' + id + '">';
                        for (var i in v2arr) {
                            theClassName = "";
                            if ($("#selectedItem_" + v2arr[i]).length > 0) {
                                theClassName = "click"
                            }
                            html += '<span id="item_' + v2arr[i][0] + '" class="lv2 ' + className + theClassName + '">' + v2arr[i][1] + "</span>"
                        }
                        html += "</div>";
                    }
                    $("#selector-lv2 .layer2").remove();
                    var a = that.index();
                    var d = a + (4 - (a + 1) % 4) % 4;
                    if (d >= $("#selector-lv2 .lv1").length) {
                        $("#selector-lv2").append(html)
                    } else {
                        $("#selector-lv2 .lv1:eq(" + d + ")").after(html)
                    }
                });

                $('#selector-lv2').off("click", ".lv2").on("click", ".lv2", function () {
                    var id = this.id.split("item_")[1];
                    var that = $(this).parent();
                    var t = $(this);

                    if ($("#item_" + id.substr(0, 4)).hasClass("click")) {
                        return false
                    } else {
                        if ($(this).hasClass("click")) {
                            $(this).removeClass("click");
                            $("#selectedItem_" + id).remove()
                        } else {
                            var html = '<span id="selectedItem_' + id + '">' + t.text() + "</span>";
                            if (onlyOne) {
                                $("#selector-lv2 .layer2 span").removeClass("click");
                                $("#selector-lv2 .lv1").removeClass("click");
                                t.addClass("click");
                                $("#selector-selected").html(html)
                            } else {
                                if ($("#selector-selected span").length >= setting.Max) {
                                    $.dialog({
                                        icon: "error",
                                        content: "最多选择" + setting.Max + "个哦",
                                        lock: true
                                    })
                                } else {
                                    t.addClass("click");
                                    $("#selector-selected").append(html)
                                }
                            }
                        }
                    }
                    updateSelect();
                });

                $("#selector-selected").off("click", "span").on("click", "span", function () {
                    var id = this.id.split("selectedItem_")[1];
                    $(this).remove();
                    $("#item_" + id).removeClass("click");
                    $("#children_" + id + " span").removeClass("click");
                    updateSelect();
                });
                defaultStandrad();
                updateSelect();
            }
            function defaultStandrad() {
                if ($("input", the).val()) {
                    var seled = $("input", the).val().split(",");
                    var k = 0;
                    var html = "";
                    for (var i in seled) {
                        var name = "";
                        if (seled[i].length == 4)
                            name = cache[seled[i]]['name'];
                        else
                        {
                            var parent = seled[i].substr(0, 4);
                            name = cache[parent]['children'][seled[i]]+"("+cache[parent]['name']+")";
//                            var html1 = '<div  class="layer2 cl" id="children_' + parent + '">';
//                            for (var i in cache[parent]['children']) {
//                                theClassName = "";
//                                if ($("#selectedItem_" + i).length > 0) {
//                                    theClassName = "click";
//                                }
//                                html1 += '<span id="item_' + i + '" class="lv2 ' + theClassName + '">' + cache[parent]['children'][i] + "</span>"
//                            }
//                            html1 += "</div>";
//                            console.log(html1);
//
//                            var that = $("#item_"+seled[i]).parent();
//                            var a = that.index();
//                            var d = a + (4 - (a + 1) % 4) % 4;
//
//                            if (d >= $("#selector-lv2 .lv1").length) {
//                                $("#selector-lv2").append(html1);
//                            } else {
//                                $("#selector-lv2 .lv1:eq(" + d + ")").after(html1);
//                            }

                        }
                        $("#item_" + seled[i]).addClass("click");
                        html += '<span id="selectedItem_' + seled[i] + '">' + name + "</span>";
                        k++;
                    }
                    $("#selector-selected").html(html);
                }
            }

            $(this).click(function (e) {
                _initSelector();
                e.preventDefault();
            }).hover(function () {
                $(this).addClass('hover');
            }, function () {
                $(this).removeClass('hover');
            });

            return $(this);
        }

    })
})(jQuery);
