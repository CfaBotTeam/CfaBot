$('.filter_bar').ready(function() {
    $('#model1 option').eq(1).prop('selected', true);
    $('#model2 option').eq(2).prop('selected', true);
    filterQuestions();
});

function filterQuestions() {
    data = {
        'model1': $('#model1')[0].selectedOptions[0].value,
        'model2': $('#model2')[0].selectedOptions[0].value,
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

function loadComparison(problem_id, model_index, model, choice_index) {
    choice_id = 'choice' + model_index + '_' + choice_index;
    select = $('#' + choice_id)[0];
    if (!select) return;
    options = select.selectedOptions;
    if (!options || options.length == 0) return;
    data = {
        'problem_id': problem_id,
        'model': model,
        'choice_index': choice_index,
        'comparison_index': select.selectedOptions[0].value
    };
    $.post("/refresh-comparison", data).done(function (reply) {
        var choice_container = $('#choice' + model_index + '_' + choice_index + '_comparison_container');
        choice_container.html(reply);
        loadSvg(model_index, choice_index);
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
    selectedModel1 = $('#model1')[0].selectedOptions[0].value;
    selectedModel2 = $('#model2')[0].selectedOptions[0].value;
    $.post("/refresh-problem", data).done(function (reply) {
          $('#problem_container').html(reply);
          loadComparison(problemId, 0, selectedModel1, 0);
          loadComparison(problemId, 1, selectedModel2, 0);
          loadComparison(problemId, 0, selectedModel1, 1);
          loadComparison(problemId, 1, selectedModel2, 1);
          loadComparison(problemId, 0, selectedModel1, 2);
          loadComparison(problemId, 1, selectedModel2, 2);
    });
}

function loadSvg(model_index, choice_index) {
    let container_name = 'choice' + model_index + '_' + choice_index + '_comparison_container';
    $("#" + container_name).css('table-layout', 'auto');
    let sentence1_container = $('#' + container_name + ' #sentence1_container');
    let sentence2_container = $('#' + container_name + ' #sentence2_container');
    let d3_svg = d3.select('#' + container_name + ' svg');
    max_width = sentence1_container.get()[0].scrollWidth;
    if (sentence2_container.get()[0].scrollWidth > max_width) {
        max_width = sentence2_container.get()[0].scrollWidth;
    }
    d3_svg.attr('width', max_width + 'px');
    var count = 0;
    sentence1_container.children("span").each(function(i) {
        let child1 = $(this);
        let scores = child1.data("scores");
        let child1_position = child1.position();
        let child1_lines = [];
        let child1_children = [];
        sentence2_container.children("span").each(function(i) {
            let child2 = $(this);
            let child2_position = child2.position();
            let score = scores[i];
            let id = "line_" + count++;
            let line = d3_svg.append("line")
                             .attr("id", id)
                             .attr("stroke", 'navy')
                             .attr("stroke-opacity", score)
                             .attr("stroke-width", 5)
                             .attr("x1", child1_position.left)
                             .attr("y1", child1_position.top)
                             .attr("x2", child2_position.left)
                             .attr("y2", child2_position.top - 40);
            child1_lines.push(id);
            child2.data("lines").push(id);
            if (score > 0) {
                child2.data("children").push(child1);
                child1_children.push(child2);
            }
        });
        child1.data("lines", child1_lines);
        child1.data("children", child1_children);
    });
    $("#" + container_name).css('table-layout', 'fixed');
}

function getSvg(token) {
    let comparison_container = $(token).parents('.choice_comparison_container');
    return d3.select(comparison_container.find('svg').get()[0]);
}

function selectToken(token) {
    let d3_svg = getSvg(token);
    lines = d3_svg.selectAll("line");
    lines.attr("stroke", 'lightgray');
    token_lines = $(token).data('lines');
    unStyleSelectedTokens(token);
    $(token).attr('class', 'selected_token');
    $(token_lines).each(function(i) {
        id = this;
        d3_svg.select("#" + id).each(function(i) {
            line = $(this);
            d3_svg.append("line")
                  .attr("id", id)
                  .attr("stroke", 'navy')
                  .attr("stroke-opacity", line.attr("stroke-opacity"))
                  .attr("stroke-width", line.attr("stroke-width"))
                  .attr("x1", line.attr("x1"))
                  .attr("y1", line.attr("y1"))
                  .attr("x2", line.attr("x2"))
                  .attr("y2", line.attr("y2"));
            this.remove();
        });
    });
    children_tokens = $(token).data('children');
    $(children_tokens).each(function(i) {
        $(this).attr('class', 'selected_child_token');
    });
    unlock_svg();
}

function selectAndLockToken(token) {
    selectToken(token);
    lock_svg(token);
}

function unselectToken(token) {
    let d3_svg = getSvg(token);
    if (is_svg_locked(token)) return;
    unStyleSelectedTokens(token);
    lines = d3_svg.selectAll("line");
    lines.attr("stroke", 'navy');
}

function unStyleSelectedTokens(token) {
    tokens = $(token).parents('.choice_comparison_container').find("span");
    tokens.attr('class', 'token');
}

function lock_svg(token) {
    container = $(token).parents('.choice_comparison_container');
    locked_contained_id = container.attr('id');
    $(document.body).data("locked-container-id", locked_contained_id);
}

function unlock_svg() {
    $(document.body).data("locked-container-id", '');
}

function is_svg_locked(token) {
    container = $(token).parents('.choice_comparison_container');
    locked_contained_id = container.attr('id');
    return $(document.body).data("locked-container-id") == locked_contained_id;
}
