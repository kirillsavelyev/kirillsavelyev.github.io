/**
 * Created by ska on 08.04.16.
 */

'use strict';

(function (window, document, $) {
        function sendComment() {
            var results = $('.comments');
            var content = $('textarea#comment_text').val();
            var post_id = $('#post_id').val();

            var request = $.ajax({
                url: 'http://127.0.0.1:5000/new_comm/' + post_id,
                type: 'POST',
                dataType: 'json',
                data: {
                    text: content
                }
            });

            request.success(function (response) {
                var result = '';
                for (var comm_id in response) {
                    var comm_data = response[comm_id];
                    result += '<div class="row">' + 
                            '<div class="col-md-10">' +
                                '<blockquote>' +
                                    '<p>' + comm_data["content"] + '</p>' +
                                    '<footer>' + comm_data["date"] + '</footer>' +
                                '</blockquote>' +
                            '</div>' + 
                        '</div>';
                }
                results.empty();
                $('#comment_text').val('');
                results.append(result);
            });
        }

        $(document).ready(function() {
            $('#new_comment').click(function() {
                sendComment();
            });
        });
    })(window, document, jQuery);
