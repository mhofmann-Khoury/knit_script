def knitscript_pg() -> str:
    return r"""
S: program;

program: head=header* statements=statement+;

header: eol eol type_id=identifier ":" value=expression eol;

declare_variable: assign=assignment eol;

assertion: "assert" exp=expression error=assert_error? eol;
@pass_second
assert_error: comma expression;

try_catch: "try" try_block=statement "catch" catch_block=statement;

print_statement: "print" exp=expression eol;

pause_statement: "pause" eol;

code_block: "{" statements=statement+ "}";

if_statement: "if" condition=expression ":" true_statement=code_block
                elifs=elif_statement*
                ("else" ":" false_statement=code_block)?;

elif_statement: "elif" exp=expression ":" stmnt=code_block;

while_statement: "while" condition=expression ":" while_block=code_block;

for_each_statement: "for" variables=identifier+[comma] "in" iters=expression+[comma] ":" block=code_block;

with_statement: "with" assigns=as_assignment+[comma] ":" block=code_block;
as_assignment: variable=identifier "as" exp=expression;

carriage_pass: "in" pass_dir=expression "direction" ":" "{" instructions=instruction_assignment+ "}";

param_list: args=identifier+[comma] comma kwargs=assignment+[comma] {3, right} |
				kwargs= assignment+[comma] {2} |
				args= identifier+[comma] {1};


function_declaration: "def" func_name=identifier "(" params=param_list? ")" ":" block=code_block;


return_statement: "return" exp=expression eol;

exp_statement: exp=expression eol;


xfer_rack: is_across="across" | dist_exp=expression "to" side_id=expression;

xfer_pass: "xfer" needles=expression+[comma] rack_val=xfer_rack bed=to_bed? slider="sliders"? eol;

@pass_inner
to_bed: "to" expression "bed";

drop_pass: "drop" needles=expression+[comma] eol;

cut_statement: "cut" exps=expression*[comma] eol;
remove_statement: "remove" exps=expression*[comma] eol;

push_statement: "push" needles=expression+[comma]  push_val=(push_to | push_dir) eol;
push_to: "to" push_val=("Front"|"Back"| "layer" expression);
push_dir: amount=expression? direction=("Forward"|"Backward");

statement: assertion {10}
            | print_statement {10}
            | try_catch {10}
            | pause_statement {10}
            | code_block {10}
            | if_statement {10}
            | while_statement {10}
            | for_each_statement {10}
            | with_statement {10}
            | carriage_pass {10}
            | xfer_pass {10}
            | drop_pass {10}
            | push_statement {10}
            | function_declaration {10}
            | return_statement {10}
            | cut_statement {10}
            | remove_statement {10}
            | declare_variable {2}
            | exp_statement {1};


assignment: var_name=identifier "=" exp=expression;

negation: "not" exp=expression;


direction_exp: "Leftward" | "Rightward"
                | "Increasing" | "Decreasing"
                | "-->" | "<--"
                | "current" | "opposite"
                | "repeat" | "reverse";

formatted_string: f_quote sections=f_string_section* quote;
f_string_section: "{" exp=expression "}" | string_value=f_string_text ;

@collect_sep
param_fill_list: param_fill_list comma expression | expression;

call_list: params=param_fill_list comma kwargs=assignment+[comma] {3, right} |
			params= param_fill_list {2} |
			kwargs= assignment+[comma] {1};

function_call: func_name=identifier "(" args=call_list? ")";

list_expression: "[" exps=expression*[comma] "]";

list_comp: "[" fill_exp=expression "for"
	spacer=every_spacer?
	variables=identifier+[comma] "in" iter_exp=expression
	comp_cond=if_comp?
	"]";

@pass_second
every_spacer: "every" ("even"|"odd"|"other"|expression);
@pass_second
if_comp: "if" expression;

dict_assign: key=expression ":" exp=expression;
dict_expression: "{" kwargs=dict_assign*[comma] "}";
dict_comp: "{" key=expression ":" value=expression
				"for" spacer=every_spacer?  variables=identifier+[comma] "in" iter_exp=expression
 				comp_cond=if_comp?
 				"}";

sliced_list: iter_exp=expression "[" start=expression? ":" end=expression? spacer=slice_spacer? "]" {4,left};
@pass_second
slice_spacer: ":" expression;

needle_instruction: inst=("knit" | "tuck" | "miss" | "split");

instruction_assignment: inst=expression needles=needle_list eol;

@collect_sep
needle_list: needle_list comma expression | expression;

accessor: exp=expression dot attribute=expression;
method_call: exp=expression dot method=function_call;
indexing: exp=expression "[" index=expression "]"{4,right};
unpack: "*" exp=expression;

gauge_exp: sheet_exp=expression "of" gauge=expression "sheets";

expression: expression "^" expression {right, 16}
            | expression "*" expression {left, 15}
            | expression "/" expression {left, 14}
            | expression "%" expression {left, 13}
            | expression "+" expression {left, 12}
            | expression "-" expression {left, 11}
            | expression "<" expression {left, 11}
            | expression "<=" expression {left, 11}
            | expression ">" expression {left, 11}
            | expression ">=" expression {left, 11}
            | expression "==" expression {left, 11}
            | expression "!=" expression {left, 11}
            | expression "is" expression {left, 11}
            | expression "in" expression {left, 11}
            | expression "and" expression {left, 11}
            | expression "or" expression {left, 11}
            | negation {11}
            | gauge_exp {11}
            | "(" expression ")" {17}
            | unpack {10}
            | float_exp {10}
            | int_exp {10}
            | formatted_string {10}
            | string {10}
            | direction_exp {10}
            | list_expression {10}
            | list_comp {10}
            | dict_expression {10}
            | dict_comp {10}
            | needle_instruction {10}
            | needle {9}
            | carrier {9}
            | sheet {9}
            | function_call {8}
            | method_call {7}
            | accessor {6}
            | indexing {5}
            | sliced_list {5}
            | identifier {4};


/*layout structure handles comments in language*/

LAYOUT: LayoutItem | LAYOUT LayoutItem | EMPTY;
LayoutItem: WS | Comment;
Comment: '/*' CorNCs '*/' | LineComment;
CorNCs: CorNC | CorNCs CorNC | EMPTY;
CorNC: Comment | NotComment | WS;

terminals
float_exp: /-?[0-9]*(\.?[0-9]+)?/;
int_exp: /-?[0-9]+/ {prefer};
comma: ",";
dot: /\./;
eol: ";";
left_right: /(Left)|(Right)/{10};
needle: /[fb]s?[0-9]+/{10};
carrier: /c[0-9]+/{10};
sheet: /s[0-9]+(:g[0-9]+)?/{10};
identifier: /[a-zA-Z_]+[0-9a-zA-Z_]*/{9};
KEYWORD: /\w+/;
string: /"[^"]*"/;
f_quote: /f"/;
quote: /"/;
f_string_text: /[^"{]+/;


/*Used to manage comments*/
WS: /\s+/;
LineComment: /\/\/.*/;
NotComment: /((\*[^\/])|[^\s*\/]|\/[^\*])+/;
    """