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