$(document).ready(function(){
    $(':checkbox').on('click', onCheck);
});

function onCheck(){
    // alert('监听到了点击')
    id = $(this).data('todo-id')
    $.post('/api/todo/'+id+'/', function(){
        location.reload();
    })
}


// 通过 $('input[id="myinput"]') 拿到定义id 为 myinput的 input 标签
// 然后通过 keypress 监听键盘事件，当回车键被按下返回 13，执行后面的代码
$(document).ready(function(){
    $('input[id="myinput"]').keypress(function(event){
        if(event.which == 13){
            // alert('已按回车Enter！')
            plan_id = $(this).next().val()

            $.post("/todo/add/"+plan_id, {todo: $(this).val()},
                    function(data){
                        // 这里可以拿到请求成功后的数据
                        $("#collapse"+plan_id).append(data)
                    });
        }
    })
})