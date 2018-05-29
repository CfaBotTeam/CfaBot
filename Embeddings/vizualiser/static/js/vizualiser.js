$('.filter_bar').ready(function() {
    filterQuestions();
});

function filterQuestions() {
    data = {
        'model': $('#model')[0].selectedOptions[0].value,
        'category': $('#category')[0].selectedOptions[0].value
    };
    $.post("/refresh-questions", data).done(function (reply) {
        let container = $('#questions_container');
        container.html(reply);
        let ul = container.children().first();
        let first_question = ul.children().first().get()[0];
        refreshProblem(first_question);
    });
}

function loadComparison(problem_id, choice_index) {
    options = $('#choice' + choice_index)[0].selectedOptions;
    if (!options || options.length == 0) return;
    data = {
        'problem_id': problem_id,
        'choice_index': choice_index,
        'comparison_index': $('#choice' + choice_index)[0].selectedOptions[0].value
    };
    $.post("/refresh-comparison", data).done(function (reply) {
          $('#choice' + choice_index + '_comparison_container').html(reply);
          loadSvg(choice_index);
    });
}

function refresh_questions_style(selected_question) {
    let lis = $('#questions_container ul>li');
    lis.each(function(i) {
        let li = $(this);
        let fontWeight = 'normal';
        if (this == selected_question) {
            fontWeight = 'bold';
        }
        li.css('font-weight', fontWeight);
    });
}

function refreshProblem(selected_question) {
    problemId = $(selected_question).data('problem-id');
    refresh_questions_style(selected_question);
    data = {'problem_id': problemId};
    $.post("/refresh-problem", data).done(function (reply) {
          $('#problem_container').html(reply);
          loadComparison(problemId, 0);
          loadComparison(problemId, 1);
          loadComparison(problemId, 2);
    });
}

function loadSvg(choice_index) {
    let container_name = 'choice' + choice_index + '_comparison_container';
    let sentence1_container = $('#' + container_name + ' .sentence1_container');
    let sentence2_container = $('#' + container_name + ' .sentence2_container');
    let d3_svg = d3.select('#' + container_name + ' .similarity_drawer');
    sentence1_container.children("span").each(function(i) {
        let scores = $(this).data("scores");
        let child1_position = $(this).position();
        sentence2_container.children("span").each(function(i) {
            let child2_position = $(this).position();
            let score = scores[i];
            d3_svg.append("line")
                  .attr("stroke", 'navy')
                  .attr("stroke-opacity", score)
                  .attr("stroke-width", 5)
                  .attr("x1", child1_position.left)
                  .attr("y1", child1_position.top)
                  .attr("x2", child2_position.left)
                  .attr("y2", child2_position.top);
        });
    });
}
