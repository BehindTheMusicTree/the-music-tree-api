/*global opener */
'use strict';
{
    const initData = JSON.parse(document.getElementById('django-admin-popup-response-constants').dataset.popupResponse);
    switch(initData.action) {
    case 'change':
        opener.dismissChangeRelatedObjectPopup(window, initData, initData.obj, initData.new_value);
        break;
    case 'delete':
        opener.dismissDeleteRelatedObjectPopup(window, initData);
        break;
    default:
        opener.dismissAddRelatedObjectPopup(window, initData, initData.obj);
        break;
    }
}
