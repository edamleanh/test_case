import { Selector } from 'testcafe';

fixture`Demo Login Test`
    .page`http://localhost:8000/accounts/login/`;

const usernameInput = Selector('#id_username');
const passwordInput = Selector('#id_password');
const logoImg = Selector('img[alt="DMOJ"][src="/static/icons/logo.svg"]');
const aceEditor = Selector('.ace_content');
const aceTextArea = Selector('textarea.ace_text-input'); 
const previewTab = Selector('a.item[data-tab="preview-tab-body"]').withText('Preview');
const postButton = Selector('input[type="submit"]').withAttribute('value', 'Post!').withAttribute('class', 'button');
const successMessage = Selector('.comment-body p').withText('Test comment');
const problemsLink = Selector('a.nav-problems[href="/problems/"]');
const firstProblemLink = Selector('#problem-table tbody tr td.problem a').nth(0);

test('User can log in with valid credentials', async t => {
    await t
        .typeText(usernameInput, 'admin')
        .typeText(passwordInput, 'Ducanh12a1@!')
        .pressKey('enter')
        .click(problemsLink)
        .click(firstProblemLink)
        .click(aceEditor)
        .typeText(aceTextArea, 'Test comment', { replace: true })
        .click(previewTab)
        .click(postButton)
        .expect(successMessage.exists).ok('Should show the posted comment as a success message')
        
});

