document.addEventListener('DOMContentLoaded', function () {
    var lessonTypeSelect = document.getElementById('session_lesson_type');
    var urlParams = new URLSearchParams(window.location.search);
    var defaultLessonType = urlParams.get('defaultLessonType');
    if (defaultLessonType && lessonTypeSelect) {
        lessonTypeSelect.value = defaultLessonType;
    }
});