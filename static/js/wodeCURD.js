// 自执行函数：
(function () {
    var requestUrl=null;

    String.prototype.format = function (kwargs) {
        var ret = this.replace(/\{(\w+)\}/g, function (km, m) {
            return kwargs[m];
        });
        return ret;
    };
    
    function bindChangePager(){
        $('#idPagination').on('click','a',function () {
            var num=$(this).text();
            init(num);
        })
    }

    function bindidSave() {
        $('#idSave').click(function () {
            var postlist=[];
            $('#table_tb').find('tr[has-edit="true"]').each(function () {
                // $(this) => 已编辑的tr
                temp={};
                temp['id']=$(this).attr('row-id');
                $(this).children('[edit-enable="true"]').each(function () {
                    //$(this) => 可编辑的td
                    var origin=$(this).attr('original-id');
                    var newval=$(this).attr('new-val');
                    var field=$(this).attr('field');
                    if (origin != newval){
                        temp[field]=newval;
                    }
                });
                postlist.push(temp);
                console.log(postlist);
            });
            $.ajax({
                url:requestUrl,
                type: 'PUT',
                data:{'postlist':JSON.stringify(postlist)}, //必为k/v类型的数据
                dataType: 'JSON',
                success:function (arg) {
                    if (arg.status){
                        init(1);   //也可以携带当前页过去
                    }else{
                        alert('error')
                    }
                },
            })
        });

    }

    function bindidReverseAll() {
        $('#idReverseAll').click(function () {
            $('#table_tb').find(':checkbox').each(function () {
                if ($('#idEditMode').hasClass('btn-warning')){
                    // reverse反选
                    if ($(this).prop('checked')){
                        $(this).prop('checked',false);
                        var $currentTr=$(this).parent().parent();
                        trOutEditMode($currentTr);
                    }else{
                        $(this).prop('checked',true);
                        var $currentTr=$(this).parent().parent();
                        trIntoEditMode($currentTr);
                    }
                }else{
                    //$(this).prop('checked',false);
                    if ($(this).prop('checked')){
                        $(this).prop('checked',false);
                    }else{
                        $(this).prop('checked',true);
                    }
                }
            })
        })
    }

    function bindidCancelAll() {
        $('#idCancelAll').click(function () {
            $('#table_tb').find(':checked').each(function () {
                if ($('#idEditMode').hasClass('btn-warning')){
                        // 去掉checkbox选中
                        $(this).prop('checked',false); //$(this)指被选中的checkbox
                        var $currentTr=$(this).parent().parent();
                        trOutEditMode($currentTr);
                }else{
                    $(this).prop('checked',false);
                }
            })
        })
    }

    function bindidCheckAll() {
        $('#idCheckAll').click(function () {
            $('#table_tb').find(':checkbox').each(function () {
                if ($('#idEditMode').hasClass('btn-warning')){
                    if ($(this).prop('checked')){
                        // 已被选中不做处理
                    }else{
                        // 进入编辑模式：
                        $(this).prop('checked',true);
                        var $currentTr=$(this).parent().parent();
                        trIntoEditMode($currentTr);
                    }
                }else{
                    $(this).prop('checked',true);
                }
            })
        })
    }

    function bindEditMode() {
        //进入编辑模式按钮绑定：
        $('#idEditMode').click(function () {
            var editing=$(this).hasClass('btn-warning');
            if (editing){
                //退出编辑模式
                $(this).removeClass('btn-warning');
                $(this).text('进入编辑模式');
                $('#table_tb').find(':checked').each(function () {
                    var $currentTr=$(this).parent().parent();

                    trOutEditMode($currentTr);
                })
            }else{
                //进入编辑模式
                $(this).addClass('btn-warning');
                $(this).text('退出编辑模式');
                $('#table_tb').find(':checked').each(function () {
                    var $currentTr=$(this).parent().parent();

                    trIntoEditMode($currentTr);
                })
            }
        })
    }

    function bindCheckbox() {
        $('#table_tb').on('click',':checkbox',function () {
            // checkbox点击
            if ($('#idEditMode').hasClass('btn-warning')){
                // alert(1);   问题：先alert还是先执行checkbox选中？ 答：先checkbox后执行下面代码*****
                var ck=$(this).prop('checked');  //prop返回属性值,注意不是返回属性
                var $currentTr=$(this).parent().parent();  //自定规则：以$开头的自定变量都是jq的选择器*******
                if (ck){
                    // 进入编辑模式
                    $currentTr.addClass('success');
                    trIntoEditMode($currentTr);
                }else{
                    // 退出编辑模式
                    $currentTr.removeClass('success');
                    trOutEditMode($currentTr);
                }
            }
        })
    }

    function trOutEditMode($currentTr) {
        $currentTr.removeClass('success');
        $currentTr.children().each(function () {
            var editEnable=$(this).attr('edit-enable'); //$(this)指代第一个外层（父亲）的对象
            var editType=$(this).attr('edit-type');
            if (editEnable == 'true'){
                // 整行退出编辑模式：
                if (editType == 'input'){
                    var $inputEle=$(this).children().first();
                    $(this).html($inputEle.val()); //jquery对象$(this)没有innerHTML属性，js中的标签则有
                    $(this).attr('new-val',$inputEle.val());
                }else if(editType == 'select'){
                    var $selectEle=$(this).children().first();
                    var $index=$selectEle.val();
                    var newValue=$selectEle[0].selectedOptions[0].innerHTML;
                    $(this).html(newValue);
                    $(this).attr('new-val',$index);
                }else{
                    //这里做输入框类型增加的扩展+++++++++++++++
                }
            }
        })
    }

    function trIntoEditMode($currentTr) {
        $currentTr.addClass('success');
        $currentTr.attr('has-edit','true');
        $currentTr.children().each(function () {
            var editEnable=$(this).attr('edit-enable'); //$(this)指代第一个外层（父亲）的对象
            var editType=$(this).attr('edit-type');
            if (editEnable == 'true'){
                // 整行进入编辑模式：
                var originalText=$(this).text();
                if (editType == 'select'){
                    // 下拉框
                    var globalName=$(this).attr('global-name'); //prop用于检索属性值仅获取属性用attr
                    var originalID=$(this).attr('original-id');
                    // 生成select
                    var sel=document.createElement('select');
                    sel.className='form-control';
                    $.each(window[globalName],function (k1,v1) {
                        var op=document.createElement('option');
                            op.setAttribute('value',v1[0]);
                            op.innerHTML=v1[1];
                            sel.append(op);
                    });
                    $(sel).val(originalID); //设置select标签中value为originalID选中
                    $(this).html(sel);

                }else if (editType == 'input'){
                    // input文本框
                    var tag=document.createElement('input'); //要考虑其他输入类型的时候
                    tag.className='form-control';
                    tag.style.width='100%';
                    tag.value=originalText;
                    //$(this).innerHTML=tag; //innerHTML这样是赋值字符串给指定标签
                    $(this).html(tag); //这个才是jquery正确的给指定标签添加子标签的方法
                }else{
                    // 这里做各种输入类型的扩展+++++++++++++++
                }
            }
        })
    }

    function init(pager) {
        $.ajax({
            url: requestUrl,
            type: 'GET',
            data:{'pager':pager},
            dataType: 'JSON',
            success: function (arg) {
                var table_config = arg.table_config;
                var table_data_list = arg.table_data_list;
                initGlobalData(arg.global_dict);
                initHeader(table_config);
                initBody(table_config, table_data_list);
                initPager(arg.pager);


            }
        })
    }

    function initPager(pager) {
        $('#idPagination').html(pager);
    }

    function initHeader(table_config) {
        $('#table_th').empty();
        var tr = document.createElement('tr');
        $.each(table_config, function (index, item) {
            var th = document.createElement('th');
            if (item.display) {
                th.innerHTML = item.title;
                tr.append(th)
            }
        });
        $('#table_th').append(tr);
    }

    function initBody(table_config, table_data_list) {
        $('#table_tb').empty();
        $.each(table_data_list, function (index, item) {
            //item={'id': 1, 'cabinet_order': '1', 'cabinet_num': '12B'}
            var tr = document.createElement('tr');
            tr.setAttribute('row-id',item['id']);
            $.each(table_config, function (i, config) {
                //config={
                //       'theme': 'cabinet_order',
                //       'title': '机柜位置',
                //       'display': True,
                //       'text': {'content': '{n}-{m}', 'kwargs': {'n': '机柜', 'm': 'xxx'}},
                //  },
                if (config.display) {
                    var td = document.createElement('td');

                    //生成文本内容：
                    var kwargs = {};
                    $.each(config.text.kwargs, function (key, value) {
                        //'text': {'content': '{n}', 'kwargs': {'n': '@@device_type_choices'}},
                        if (value.substring(0, 2) == '@@') {
                            var global_name = value.substring(2, value.length);
                            var id_num = item[config.theme];
                            kwargs[key] = getTextFromGlobalByID(global_name, id_num);
                        } else if (value[0] == '@') {
                            kwargs[key] = item[value.substring(1, value.length)]; //substring是切片的意思
                        } else {
                            kwargs[key] = value;
                        }
                    });
                    var temp = config.text.content.format(kwargs);
                    td.innerHTML = temp;
                    //td.innerText=item[config.theme];

                    //配置属性：

                    //'attrs': {'original-id':'@device_status_id','edit-enable': 'true', 'edit-type': 'select', 'global-name': 'device_status_choices'},
                    $.each(config.attrs,function (k,v) {
                        if (v[0] == '@'){
                            td.setAttribute(k,item[v.substring(1,v.length)]);
                        }else{
                            td.setAttribute(k,v);
                        }
                    });
                    tr.append(td);
                }
            });
            $('#table_tb').append(tr);
        });
    }

    function initGlobalData(global_dict) {
        $.each(global_dict, function (k, v) {
            window[k] = v;
            // 这个就是设置字符串为全局变量
        })
    }

    function getTextFromGlobalByID(global_name, id_num) {
        var ret=null;
        $.each(window[global_name], function (x, y) {
            if (y[0] == id_num) {
                ret=y[1];
                return //只终止each循环*****
            }
        });
        if (ret){
            return ret;
        }else{
            return '数据错误';
        }
    }

    jQuery.extend({
        'NB':function (url) {
            requestUrl=url;
            init(); //放数据的
            bindEditMode(); //给按钮绑定事件
            bindCheckbox(); //给选项列的checkbox绑定事件
            bindidCheckAll(); //给全选按钮绑定事件
            bindidCancelAll(); //给取消按钮绑定事件
            bindidReverseAll(); //给取消按钮绑定事件
            bindidSave(); //给保存按钮绑定事件
            bindChangePager(); //给页码绑定事件
        },
        'changePager':function (num) {
            init(num);
        }
    });
})();
