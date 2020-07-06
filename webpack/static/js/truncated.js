function text_truncate(){
    var str = document.getElementById("truncated_title").innerHTML;
    var length = 30;
    var ending = '...';
    if (str.length > length) {
      str = str.substring(0, length - ending.length) + ending;
    } else {
      str = str;
    }
    document.getElementById("truncated_title").innerHTML = str;
}