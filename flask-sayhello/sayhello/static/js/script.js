$(function () {
    function render_time() {
        return moment($(this).data('timestamp')).format('lll')
    }
    $('[data-toggle="tooltip"]').tooltip(
        {title: render_time}
    );
});
// 设置显示绝对时间的弹窗 tooltip
// data-toggle 属性作为选择器选择所有设置了 tooltip 属性的元素
// title 选项设置弹出内容，字符串或者函数对象