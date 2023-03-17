#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define clrscr() system("cls")
#define LOOP 8 145060

int main()
{

int i, j, k, l, max, maxid, lotto[6], arr[46] = {0};
time_t t;

srand((unsigned)time(&t));
//시간을 참조하여 랜덤표 만듦
    for(i=0;i<LOOP;i++)
    {
        printf("\n\t ========== Lotto 추첨중 ========== %8d회 \n", i);
        printf("\n\t Lotto 추첨번호 : ");
        for(j=0;j<6;j++)
        {
            lotto[j]=(rand()%45)+1;
            for(k=0;k<j;k++)
            {
                if(lotto[k]==lotto[j])
                {
                    lotto[j]=(rand()%45)+1;
                    k=-1;
                    continue;
                }
            }
            printf("%3d", lotto[j]);
            arr[lotto[j]]++;
        }
        puts("\n");
        for(l=1;l<46;l++)
        {
            printf("  %2d = %8d%s", l, arr[l], (l%5)==0?"\n":"");
        }
        if(i!=LOOP-1)
            clrscr();
    }
    puts("\n");

    printf("\t===== 최다 출현 번호 =====\n\n");
for(i=1;i<=6;i++)
{
max = 0;
for(j=1; j<46; j++)
{
if(max < arr[j])
{
maxid=j;
max=arr[j];
}
}
printf("\t %d %3d => %8d\n", i, maxid, max);
arr[maxid] = 0;
}
return 0;
}
