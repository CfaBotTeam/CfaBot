$('.filter_bar').ready(function() {
    $('#file1 option').eq(2).prop('selected', true);
    filterQuestions();
});

function filterQuestions() {
    data = {
        'file1': $('#file1')[0].selectedOptions[0].value,
        'category': $('#category')[0].selectedOptions[0].value
    };
    $.post("/refresh-questions", data).done(function (reply) {
        let container = $('#questions_container');
        container.html(reply);
        let first_question = container.find('#questions_list .question').first().get()[0]
        refreshProblem(first_question);
    });
}

function loadComparison(problem_id, file_index, filename, model, choice_index, question_index) {
    choice_id = 'choice' + file_index + '_' + choice_index;
    select = $('#' + choice_id)[0];
    if (!select) return;
    options = select.selectedOptions;
    if (!options || options.length == 0) return;
    data = {
        'problem_id': problem_id,
        'filename': filename,
        'model': model,
        'question_index': question_index,
        'choice_index': choice_index,
        'comparison_index': select.selectedOptions[0].value
    };
    $.post("/refresh-comparison", data).done(function (reply) {
        var choice_left_id = '.choice' + file_index + '_' + choice_index + '_comparison_left';
        var container = $(choice_left_id + ' .choice_comparison_container');
        container.html(reply['html']);
        $(choice_left_id + ' .q_source_container').html(reply['q_source']);
        $(choice_left_id + ' .c_source_container').html(reply['c_source']);
        loadSvg(container);
    });
}

function changeComparison(problem_id, file_index, filename, choice_index, question_index) {
    if (file_index == 0) {
        model = $('#model1_container').get()[0].innerText;
    } else {
        model = $('#model2_container').get()[0].innerText;
    }
    loadComparison(problem_id, file_index, filename, model, choice_index, question_index);
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
    selectedFile1 = $('#file1').val();
    data = {
        'problem_id': problemId,
        'file1': selectedFile1,
    };
    if ($('#file2').val() != 'None') {
        selectedFile2 = $('#file2').val();
        data['file2'] = selectedFile2;
    }
    $.post("/refresh-problem-details", data).done(function (reply) {
        $('#problem_details').html(reply);
    });
    $.post("/refresh-problem-choices", data).done(function (reply) {
        $('#choices_container').html(reply);
    });
    $.post("/refresh-problem", data).done(function (reply) {
        $('#problem_container').html(reply['html']);
        let model1 = reply['model1'];
        $('#model1_container').html(model1);
        $('#dataset_container').html(reply['dataset']);
        $('#provider_container').html(reply['provider']);
        $('#glossary_container').html(reply['glossary']);
        loadComparison(problemId, 0, selectedFile1, model1, 0, 0);
        loadComparison(problemId, 0, selectedFile1, model1, 1, 0);
        loadComparison(problemId, 0, selectedFile1, model1, 2, 0);
        loadComparison(problemId, 0, selectedFile1, model1, 3, 0);

        let model2 = reply['model2'];
        if (model2) {
            $('#model2_container').html(model2);
            loadComparison(problemId, 1, selectedFile2, model2, 0, 0);
            loadComparison(problemId, 1, selectedFile2, model2, 1, 0);
            loadComparison(problemId, 1, selectedFile2, model2, 2, 0);
            loadComparison(problemId, 1, selectedFile2, model2, 3, 0);
        }
    });
}

function loadSvg(container) {
    container.css('table-layout', 'auto');
    let sentence1_container = container.find('#sentence1_container');
    let sentence2_container = container.find('#sentence2_container');
    let svg = container.find('svg');
    let d3_svg = d3.select(svg.get()[0]);
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
    container.css('table-layout', 'fixed');
}

function getSvg(token) {
    let comparison_container = $(token).parents('.choice_comparison_container');
    return d3.select(comparison_container.find('svg').get()[0]);
}

function selectToken(token) {
    let d3_svg = getSvg(token);
    lines = d3_svg.selectAll("line");
    lines.attr("stroke", 'gainsboro');
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
