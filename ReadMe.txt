#  --tsv can be used in the pipeline to produce tsv files directly. Note that some fields are in the RDS that are not saved in the tsv
# qlogin -l h_rt=20:00:00 -l h_vmem=50G -pe threaded 6
cd ~/bulk/My_Works/Translocation_Identification_Using_4C/10_Adrien_Translocation_Detection/side_analysis/07_PK_4CPipeline_newVersion

rn=PeakC_data;
cmd="module load R/3.5.1; cd ./side_analysis/07_PK_4CPipeline_newVersion/; Rscript pipe4C.R -vpFile ../../fastqs/${rn}/vp_info.txt -fqFolder ../../fastqs/${rn}/DeMux/ -outFolder ./Output/${rn}/ -readsQuality 1 -cores 6 --plot"
qsub -P hub_laat -N prc_${rn} -l h_rt=30:00:00 -l h_vmem=20G -pe threaded 6 ~/bulk/bin/run_script.sh $cmd

rn=SE_2015_11_Cuppen;
rn=SE_2015_12_Cuppen;
rn=WDLA044;
cmd="module load R/3.5.1; cd ./side_analysis/07_PK_4CPipeline_newVersion/; Rscript pipe4C.R -vpFile ../../fastqs/${rn}/vp_info.txt -fqFolder ../../fastqs/${rn}/ -outFolder ./Output/${rn}/ -readsQuality 1 -cores 6 --plot"
qsub -P hub_laat -N prc_${rn} -l h_rt=30:00:00 -l h_vmem=20G -pe threaded 6 ~/bulk/bin/run_script.sh $cmd

# VER2800
ti=1; 
cmd="module load R/3.5.1; cd ./side_analysis/07_PK_4CPipeline_newVersion/; Rscript pipe4C.R -vpFile ../../fastqs/VER2800/VER2800Truseq${ti}_vpinfo.txt -fqFolder ../../fastqs/VER2800/ -outFolder ./Output/VER2800Truseq${ti}/ -readsQuality 1 -cores 6 --plot --tsv"
qsub -P hub_laat -N prc_VEr2800_${ti} -l h_rt=30:00:00 -l h_vmem=20G -pe threaded 6 ~/bulk/bin/run_script.sh $cmd

# Some VER2800 runs do not produce any reads, the sequence given seems to be wrong. VP info is adjusted accordingly:
cmd="module load R/3.5.1; cd ./side_analysis/07_PK_4CPipeline_newVersion/; mkdir ./Output/VER2800_AdjustedSeqs/; Rscript pipe4C.R -vpFile ../../fastqs/VER2800/AdjustedSeqs_vpinfo.txt -fqFolder ../../fastqs/VER2800/ -outFolder ./Output/VER2800_AdjustedSeqs/ -readsQuality 1 -cores 6 --plot --tsv"
qsub -P hub_laat -N VER2800_AdjustedSeqs -l h_rt=30:00:00 -l h_vmem=20G -pe threaded 6 ~/bulk/bin/run_script.sh $cmd
The pipeline seems to require having restriction enzyme to be seen in the read, therefore it fails on vp-distance= 108kb runs. I changed the sequence to correct one using:
zcat MOLT16_M16_14_108kb_HD_800ng_2pct.fastq.gz | sed s/^GAATAGTAGAGGCTGCCATGAAGCCT/GAATAGTAGAGGCTGCCATGAAGCTT/ | gzip >    MOLT16_M16_14_108kb_HD_800ng_2pct_new.fastq.gz


# MN00149_0243
rn=MN00149_0243;
cmd="module load R/3.5.1; cd ./side_analysis/07_PK_4CPipeline_newVersion/; Rscript pipe4C.R -vpFile ../../fastqs/${rn}/vp_info.txt -fqFolder ../../fastqs/${rn}/ -outFolder ./Output/${rn}/ -readsQuality 1 -cores 6 --plot"
qsub -P hub_laat -N prc_${rn} -l h_rt=30:00:00 -l h_vmem=20G -pe threaded 6 ~/bulk/bin/run_script.sh $cmd


# VER3386
rn=VER3386;
cmd="module load R/3.5.1; cd ./side_analysis/07_PK_4CPipeline_newVersion/; Rscript pipe4C.R -vpFile ../../fastqs/${rn}/vp_info.txt -fqFolder ../../fastqs/${rn}/ -outFolder ./Output/${rn}/ -readsQuality 1 -cores 6 --plot"
qsub -P hub_laat -N prc_${rn} -l h_rt=30:00:00 -l h_vmem=20G -pe threaded 6 ~/bulk/bin/run_script.sh $cmd
