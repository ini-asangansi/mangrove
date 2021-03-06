(function(content, linkDests, _opts){
    var modeSlugs = $.map(linkDests, function(i, b){return i[1];});
    var defaultOpts = {defaultMode: modeSlugs[0]};
    var opts = $.extend({}, _opts, defaultOpts);
    content.bind('modeChange', function(evt, md){
    	var mode = md.mode;
    	$.cookie('mode', mode);
    	content.data('mode', mode);
    	$.each(linkDests, function(i, cln){
    		if(cln[1]==mode) {content.addClass(cln[1]);} else {content.removeClass(cln[1]);}
    	});
    	$('p.region-breadcrumbs').find('a.mode-link').each(function(i, e){
    		var z = $(e).data('link-dest');
    		if(z==mode) {
    			$(e).addClass('selected');
    		} else {
    			$(e).removeClass('selected');
    		}
    	});
    });

    /* Add mode breadcrumbs if the breadcrumb wrap exists
    */
    var bcs = $('p.region-breadcrumbs');
    if(bcs.length>0) {
        function clickCoolLink(evt) {
    		var modeDest = $(this).data('link-dest');
    		if(modeDest!==undefined) {
    			content.trigger('modeChange', {'mode':modeDest});
    		}
    		$(this).blur();
    		evt.preventDefault();
    	}
        function coolifyButton(l){
            var hw = [l.outerHeight(), l.outerWidth()];
    		l.wrapInner("<span class='a' />");
    		var b = $("<span />", {'class':'b'}).css({display:'block', height: hw[0], width: hw[1]});
    		var c = $("<span />", {'class':'c'}).css({display:'block', height: hw[0], width: hw[1]});
    		l.append(b);
    		l.append(c);
        }
        $.each(linkDests.reverse(), function(i, ld){
            var button = $('<a />', {'href':'#', 'class': 'mode-link'}).text(ld[0]).data('link-dest', ld[1]).click(clickCoolLink);
            button.hide();
            bcs.append(button);
            coolifyButton(button);
        });
        $('a', bcs).show()
    }
    
    /* Add mode breadcrumbs if the breadcrumb wrap exists
    */
    if(~modeSlugs.indexOf($.cookie('mode'))) {
    	content.trigger('modeChange', {mode:$.cookie('mode')});
    } else if(content.data('mode')==undefined) {
    	content.trigger('modeChange', {mode:opts.defaultMode});
    }
})($('#content'), [
            ["Facilities", "facilities"],
            ["MDG Indicators", "mdg-indicators"]
        ]);

/*-- Mark "activity status" on region nav objects...
--*/
$(function(){
    var statii = ["inactive", "phase-one", "phase-two"];
    $('a.region-nav').each(function(){
        var activityStatus = $(this).data('activityStatus');
        if(activityStatus!==undefined && activityStatus.scaleupStatus!==undefined) {
            var scaleupStatus = activityStatus.scaleupStatus;
            $(this).addClass('scaleup-'+statii[scaleupStatus]);
        }
    });
});

(function(sInput){
    var searchText = "search";
    if(sInput.val()=='') {
        sInput.val(searchText);
        sInput.addClass('inactive');
    }
    sInput.focus(function(){
        if($(this).val()==searchText) {
            $(this).val('');
            $(this).removeClass('inactive');
        }
    });
    sInput.blur(function(){
        if($(this).val()==='') {
            $(this).val(searchText);
            $(this).addClass('inactive');
        }
    })
})($('.search-box input'));
